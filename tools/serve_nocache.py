from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os

WEBAPP_DIR = r"C:\Users\user\Desktop\words-app\webapp"


class NoCacheHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBAPP_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8088), NoCacheHandler)
    print("Serving webapp with no-cache headers on http://127.0.0.1:8088")
    server.serve_forever()
