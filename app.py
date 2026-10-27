from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info("Request received: %s", self.path)

        if self.path == "/":
           body = b"DevOps Lab Application is running successfully!\n"
            status = 200
            content_type = "text/plain"

        elif self.path == "/health":
            body = b'{"status":"healthy"}\n'
            status = 200
            content_type = "application/json"

        elif self.path == "/metrics":
            body = (
                "# HELP devops_app_up Application availability\n"
                "# TYPE devops_app_up gauge\n"
                "devops_app_up 1\n"
            ).encode()
            status = 200
            content_type = "text/plain; version=0.0.4"

        elif self.path == "/error":
            body = b'{"error":"Intentional test error"}\n'
            status = 500
            content_type = "application/json"
            logging.error("Intentional test error requested")

        else:
            body = b'{"error":"Not found"}\n'
            status = 404
            content_type = "application/json"

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), AppHandler)
    logging.info("Server started on port 8000")
    server.serve_forever()
