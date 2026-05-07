
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from twilio.twiml.messaging_response import MessagingResponse

BLOCKED_NUMBERS = {
    "+19653634683",
    "+14053433154",
    "+18653634683"
}

class SMSHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/sms":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()

        data = parse_qs(body)
        from_number = data.get("From", [""])[0]

        resp = MessagingResponse()

        if from_number in BLOCKED_NUMBERS:
            resp.message("You are blocked")

        response_xml = str(resp)

        self.send_response(200)
        self.send_header("Content-Type", "text/xml")
        self.send_header("Content-Length", str(len(response_xml)))
        self.end_headers()
        self.wfile.write(response_xml.encode())

def run():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SMSHandler)
    print(f"Listening on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
