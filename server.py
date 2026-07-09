import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pypresence import Presence

# 1. Replace with your Discord Application ID from the Developer Portal
CLIENT_ID = "152464373412843122"

print("Initializing Discord Rich Presence...")
try:
    RPC = Presence(152464373412843122)
    RPC.connect()
    print("Successfully connected to Discord Gateway!")
except Exception as e:
    print(f"Could not connect to Discord. Error: {e}")
    RPC = None

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        song = data.get("song", "Unknown Song")
        artist = data.get("artist", "Unknown Artist")
        
        print(f"Received from phone: {song} by {artist}")
        
        # Update Discord Profile Status
        if RPC:
            RPC.update(
                details=f"🎵 {song}",
                state=f"🎤 {artist}",
                activity_type=2 # 2 = "Listening to"
            )
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Status updated successfully")

def run():
    # Listens on port 8080 for your phone's web pings
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, WebhookHandler)
    print("Cloud bridge server is running on port 8080...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
