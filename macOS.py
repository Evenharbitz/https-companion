import http.server
import subprocess
import socketserver
import socket
import os
def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    ip_address = sock.getsockname()[0]
    sock.close()
    return ip_address
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        def endrequest():
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
        if self.path.startswith ("/generic="):
            cmd = self.path.split('=')[1]
            if cmd == "sleep":
                subprocess.run(['pmset', 'sleepnow'])
                endrequest()
        elif self.path.startswith ("/quit="):
            quitapp = self.path
            app_name = quitapp.split('=')[1]
            app_words = app_name.split('%20')
            app_to_quit = ' '.join(app_words)
            subprocess.run(['pkill', '-x', app_to_quit])
            endrequest()
        elif self.path.startswith ('/web='):
            sitename = self.path.split('=')[1]
            sitename = 'https://' + sitename
            subprocess.run(['open', sitename])
            endrequest()
        elif self.path.startswith ('/ip='):
            ip = self.path.split('=')[1]
            ip = 'http://' + ip
            subprocess.run(['open', ip])
            endrequest()
        elif self.path.startswith('/openprogram?program='):
            openapp = self.path
            app_name = openapp.split('=')[1]
            app_words = app_name.split('%20')
            app_to_open = ' '.join(app_words)
            subprocess.run(['open', '-a', app_to_open])
            endrequest()
        else:
            self.wfile.write(b'404 Not Found')
local_ip = get_local_ip()
print(f"IP: {local_ip}")
def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = (local_ip, port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://{local_ip}:{port}")
    httpd.serve_forever()
if __name__ == '__main__':
    run()