#!/usr/bin/env python3
"""
Lightweight proxy: translates OpenAI-compatible API calls to Ollama native API
with think:false, then translates responses back to OpenAI format.

Uses non-streaming Ollama requests internally and converts to SSE for clients.

Usage: python3 ollama_nothink_proxy.py [listen_port] [ollama_port]
  Default: listens on 11436, forwards to 127.0.0.1:11435
"""
import http.server, json, sys
import requests as req_lib

OLLAMA_PORT = sys.argv[2] if len(sys.argv) > 2 else "11435"
OLLAMA_URL = f"http://127.0.0.1:{OLLAMA_PORT}"
LISTEN_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 11436

SESSION = req_lib.Session()


def normalize_messages(messages):
    """Convert OpenAI message format to Ollama native format.

    Also applies a trailing-space workaround for assistant messages to avoid
    an Ollama ≤0.17 JSON-parsing bug triggered by certain content patterns.
    """
    normalized = []
    for msg in messages:
        out = {"role": msg.get("role", "user")}

        content = msg.get("content")
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(part.get("text", ""))
                elif isinstance(part, str):
                    text_parts.append(part)
            out["content"] = "\n".join(text_parts) if text_parts else ""
        elif content is None:
            out["content"] = ""
        else:
            out["content"] = content

        # Workaround: Ollama ≤0.17 has a JSON-parsing bug triggered by certain
        # assistant message content (e.g. "Got it. Thanks for the context!").
        # Appending a trailing space to non-empty assistant content avoids it.
        if out["role"] == "assistant" and out["content"] and not out["content"].endswith(" "):
            out["content"] += " "

        if msg.get("tool_calls"):
            normalized_tc = []
            for tc in msg["tool_calls"]:
                ntc = dict(tc)
                if "function" in ntc:
                    func = dict(ntc["function"])
                    args = func.get("arguments", {})
                    if isinstance(args, str):
                        try:
                            func["arguments"] = json.loads(args)
                        except (json.JSONDecodeError, TypeError):
                            func["arguments"] = {}
                    ntc["function"] = func
                normalized_tc.append(ntc)
            out["tool_calls"] = normalized_tc

        if msg.get("role") == "tool" and msg.get("tool_call_id"):
            out["tool_call_id"] = msg["tool_call_id"]

        if msg.get("name"):
            out["name"] = msg["name"]

        normalized.append(out)
    return normalized


def ollama_tool_calls_to_openai(tool_calls):
    """Convert Ollama tool_calls to OpenAI format."""
    result = []
    for i, tc in enumerate(tool_calls):
        result.append({
            "index": i,
            "id": f"call_{tc.get('function', {}).get('name', 'unknown')}_{i}",
            "type": "function",
            "function": {
                "name": tc.get("function", {}).get("name", ""),
                "arguments": json.dumps(tc.get("function", {}).get("arguments", {})),
            }
        })
    return result


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        try:
            r = SESSION.get(f"{OLLAMA_URL}{self.path}", timeout=10)
            self.send_response(r.status_code)
            self.send_header("Content-Type", r.headers.get("Content-Type", "application/json"))
            self.end_headers()
            self.wfile.write(r.content)
        except Exception as e:
            self.send_error(502, str(e)[:200])

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        body = json.loads(raw)

        if "/v1/chat/completions" not in self.path:
            self._forward_raw(raw)
            return

        client_wants_streaming = body.get("stream", False)

        native = {
            "model": body.get("model", ""),
            "messages": normalize_messages(body.get("messages", [])),
            "stream": False,
            "think": False,
        }

        opts = {}
        if "temperature" in body:
            opts["temperature"] = body["temperature"]
        if "max_tokens" in body:
            opts["num_predict"] = body["max_tokens"]
        if "top_p" in body:
            opts["top_p"] = body["top_p"]
        if "stop" in body:
            opts["stop"] = body["stop"]
        if body.get("tools"):
            native["tools"] = body["tools"]
        if opts:
            native["options"] = opts

        try:
            native_bytes = json.dumps(native).encode("utf-8")
            r = SESSION.post(f"{OLLAMA_URL}/api/chat", data=native_bytes,
                             headers={"Content-Type": "application/json"}, timeout=900)

            # Retry strategies for Ollama JSON-parse bug
            if r.status_code == 500 and "parse JSON" in r.text:
                # Strategy 1: pad all message content with trailing whitespace
                print(f"[PROXY] JSON-parse error — retry 1: pad content", flush=True)
                for m in native["messages"]:
                    c = m.get("content", "")
                    if c:
                        m["content"] = c.rstrip() + "  \n"
                native_bytes = json.dumps(native).encode("utf-8")
                r = SESSION.post(f"{OLLAMA_URL}/api/chat", data=native_bytes,
                                 headers={"Content-Type": "application/json"}, timeout=900)

            if r.status_code == 500 and "parse JSON" in r.text:
                # Strategy 2: replace all assistant history with generic text
                print(f"[PROXY] JSON-parse error — retry 2: replace assistant msgs", flush=True)
                for m in native["messages"]:
                    if m.get("role") == "assistant":
                        if m.get("content"):
                            m["content"] = "Understood."
                native_bytes = json.dumps(native).encode("utf-8")
                r = SESSION.post(f"{OLLAMA_URL}/api/chat", data=native_bytes,
                                 headers={"Content-Type": "application/json"}, timeout=900)

            if r.status_code == 500 and "parse JSON" in r.text:
                # Strategy 3: truncate tool result content (keep first 2000 chars)
                print(f"[PROXY] JSON-parse error — retry 3: truncate tool results", flush=True)
                for m in native["messages"]:
                    if m.get("role") == "tool" and len(m.get("content", "")) > 2000:
                        m["content"] = m["content"][:2000] + "\n... (truncated)"
                native_bytes = json.dumps(native).encode("utf-8")
                r = SESSION.post(f"{OLLAMA_URL}/api/chat", data=native_bytes,
                                 headers={"Content-Type": "application/json"}, timeout=900)

            if r.status_code != 200:
                # Final fallback: forward original request to Ollama's OpenAI endpoint
                # Thinking won't be suppressed but at least the request won't fail
                print(f"[PROXY] All native retries failed — falling back to OpenAI endpoint", flush=True)
                openai_body = dict(body)  # use original OpenAI-format body
                openai_body["stream"] = False
                try:
                    r2 = SESSION.post(f"{OLLAMA_URL}/v1/chat/completions",
                                      json=openai_body, timeout=900)
                    if r2.status_code == 200:
                        oai_data = r2.json()
                        msg_oai = oai_data.get("choices", [{}])[0].get("message", {})
                        # Build a fake native response for consistent downstream handling
                        data = {
                            "message": msg_oai,
                            "done_reason": oai_data.get("choices", [{}])[0].get("finish_reason", "stop"),
                            "prompt_eval_count": oai_data.get("usage", {}).get("prompt_tokens", 0),
                            "eval_count": oai_data.get("usage", {}).get("completion_tokens", 0),
                        }
                        print(f"[PROXY] OpenAI fallback succeeded ({data['eval_count']} tokens)", flush=True)
                    else:
                        print(f"[PROXY] OpenAI fallback also failed: {r2.status_code}", flush=True)
                        with open("/tmp/proxy_fail.json", "wb") as f:
                            f.write(native_bytes)
                        self.send_error(502, f"Ollama error {r.status_code}")
                        return
                except Exception as e2:
                    print(f"[PROXY] OpenAI fallback error: {e2}", flush=True)
                    self.send_error(502, f"Ollama error {r.status_code}")
                    return
            else:
                data = r.json()
        except Exception as e:
            print(f"[PROXY] Error: {e}", flush=True)
            try:
                self.send_error(502, f"Proxy error: {str(e)[:100]}")
            except Exception:
                pass
            return

        msg = data.get("message", {})
        content = msg.get("content", "")
        tool_calls = None
        if msg.get("tool_calls"):
            tool_calls = ollama_tool_calls_to_openai(msg["tool_calls"])

        finish = "stop"
        if tool_calls:
            finish = "tool_calls"
        elif data.get("done_reason") == "length":
            finish = "length"

        usage = {
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": data.get("eval_count", 0),
            "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
        }

        if client_wants_streaming:
            self._send_sse(native["model"], content, tool_calls, finish, usage)
        else:
            self._send_json(native["model"], content, tool_calls, finish, usage)

    def _send_json(self, model, content, tool_calls, finish, usage):
        resp = {
            "id": "chatcmpl-proxy",
            "object": "chat.completion",
            "model": model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": finish,
            }],
            "usage": usage,
        }
        if tool_calls:
            resp["choices"][0]["message"]["tool_calls"] = tool_calls

        out = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def _send_sse(self, model, content, tool_calls, finish, usage):
        self.close_connection = True
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        try:
            delta = {}
            if content:
                delta["content"] = content
            if tool_calls:
                delta["tool_calls"] = tool_calls

            if delta:
                chunk = {
                    "id": "chatcmpl-proxy",
                    "object": "chat.completion.chunk",
                    "model": model,
                    "choices": [{"index": 0, "delta": delta, "finish_reason": None}],
                }
                self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
                self.wfile.flush()

            final = {
                "id": "chatcmpl-proxy",
                "object": "chat.completion.chunk",
                "model": model,
                "choices": [{"index": 0, "delta": {}, "finish_reason": finish}],
                "usage": usage,
            }
            self.wfile.write(f"data: {json.dumps(final)}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()
        except BrokenPipeError:
            pass  # Client disconnected (timeout) — expected

    def _forward_raw(self, raw_body):
        try:
            r = SESSION.post(f"{OLLAMA_URL}{self.path}", data=raw_body,
                             headers={"Content-Type": "application/json"}, timeout=900)
            self.send_response(r.status_code)
            self.send_header("Content-Type", r.headers.get("Content-Type", "application/json"))
            self.end_headers()
            self.wfile.write(r.content)
        except Exception as e:
            self.send_error(502, str(e)[:200])


class ThreadedServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    server = ThreadedServer(("127.0.0.1", LISTEN_PORT), ProxyHandler)
    print(f"NoThink proxy: 127.0.0.1:{LISTEN_PORT} -> {OLLAMA_URL} (think=false)", flush=True)
    server.serve_forever()
