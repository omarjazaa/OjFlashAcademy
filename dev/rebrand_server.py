import http.server
import socketserver
import os

PORT = 8000
# Serve the repository root; the site is published at the /OjFlashAcademy/ path
# (GitHub project pages: https://omarjazaa.github.io/OjFlashAcademy/)
SITE_PREFIX = "/OjFlashAcademy"
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Prevent browser caching during local development
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        if self.path in ("", "/", "/academy", "/academy/"):
            self.send_response(302)
            self.send_header("Location", SITE_PREFIX + "/")
            self.end_headers()
            return
        
        clean_path = self.path.split("?")[0].split("#")[0]
        fs_path = os.path.join(DIRECTORY, clean_path.lstrip("/"))
        
        if clean_path.startswith(SITE_PREFIX):
            rel = clean_path[len(SITE_PREFIX):] or "/"
            fs_path = os.path.join(DIRECTORY, rel.lstrip("/"))
            if not os.path.exists(fs_path) or (os.path.isdir(fs_path) and not os.path.exists(os.path.join(fs_path, "index.html"))):
                self.path = "/index.html"
            else:
                self.path = rel
                
        return super().do_GET()

with http.server.ThreadingHTTPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}{SITE_PREFIX}/")
    httpd.serve_forever()