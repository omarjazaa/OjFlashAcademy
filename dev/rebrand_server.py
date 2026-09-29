import http.server
import socketserver
import os

PORT = 8000
# Serve the repository root (contains the academy/ site folder + root-level qr-code.png)
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
        if self.path == "/" or self.path == "":
            self.send_response(302)
            self.send_header("Location", "/academy/")
            self.end_headers()
            return
        
        clean_path = self.path.split("?")[0].split("#")[0]
        fs_path = os.path.join(DIRECTORY, clean_path.lstrip("/"))
        
        if clean_path.startswith("/academy"):
            if not os.path.exists(fs_path):
                self.path = "/academy/index.html"
            elif os.path.isdir(fs_path) and not os.path.exists(os.path.join(fs_path, "index.html")):
                self.path = "/academy/index.html"
                
        return super().do_GET()

with http.server.ThreadingHTTPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()