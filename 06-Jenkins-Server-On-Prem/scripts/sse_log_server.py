#!/usr/bin/env python3
import argparse
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class SSEHandler(BaseHTTPRequestHandler):
    log_file = None

    def do_GET(self):
        if self.path not in ("/events", "/events/"):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        while not os.path.exists(self.log_file):
            time.sleep(0.5)

        try:
            with open(self.log_file, "r", encoding="utf-8", errors="replace") as f:
                # stream from beginning so install sequence is visible to late clients too
                while True:
                    line = f.readline()
                    if line:
                        payload = line.rstrip("\r\n")
                        self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                        self.wfile.flush()
                    else:
                        time.sleep(0.3)
        except (BrokenPipeError, ConnectionResetError):
            return

    def log_message(self, fmt, *args):
        return


def main():
    parser = argparse.ArgumentParser(description="SSE log streamer")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18080)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    SSEHandler.log_file = args.log_file
    server = ThreadingHTTPServer((args.host, args.port), SSEHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
