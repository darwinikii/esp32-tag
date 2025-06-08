from util.local_devices import get_local_devices
from util.devices import get_local_device_locations
import http.server
import socketserver
import json
from urllib.parse import urlparse

local_devices = get_local_devices()

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        # İsteklerde kullanılabilecek HTTP metodlarını belirt (isteğe bağlı ama önerilir)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        # İsteklerde kullanılabilecek başlıkları belirt (isteğe bağlı ama önerilir)
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/":
            #send index.html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('../website/index.html', 'rb') as file:
                self.wfile.write(file.read())

        elif path == "/devices":
            self._send_json_response(200, local_devices)
        elif path.startswith("/device/"):
            parts = path.split('/')
            if len(parts) == 3 and parts[1] == "device":
                device_hash = parts[2]
                if device_hash in local_devices:
                    local_device_locations = get_local_device_locations(device_hash)    
                    self._send_json_response(200, local_device_locations)
                else:
                    self._send_json_response(404, {"error": "Device not found"})
            else:
                self._send_json_response(400, {"error": "Invalid device path"})
        else:
            self._send_json_response(404, {"error": "Not Found"})

    def _send_json_response(self, status_code, data):
        self._set_headers(status_code, 'application/json')
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_server(port=8000):
    handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"serving at port {port}")
        print("To test:")
        print(f"  GET /: http://localhost:{port}/")
        print(f"  GET /devices: http://localhost:{port}/devices")
        print(f"  GET /device/:device_hash (e.g., abc123def456): http://localhost:{port}/device/abc123def456")
        httpd.serve_forever()
if __name__ == '__main__':
    run_server()