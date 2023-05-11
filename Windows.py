import http.server
import subprocess
import socketserver
import socket
import os
import ctypes


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

        if self.path.startswith('/quit='):
            app = self.path.split('=')[1]
            subprocess.call(['taskkill', '/F', '/IM', app+'.exe'])
            endrequest()

        elif self.path.startswith('/generic='):
            if self.path.split('=')[1] == 'sleep':
                ctypes.windll.user32.LockWorkStation()
            endrequest()

        elif self.path.startswith('/openprogram?program='):
            program = self.path.split('=')[1]
            program = program + '.exe'
            subprocess.Popen(f'start {program}', shell=True)
            endrequest()


        else:
            self.send_response(404)

local_ip = get_local_ip()
print(f"IP: {local_ip}")

def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = (local_ip, port)
    httpd = server_class(server_address, handler_class)
    print(f"http://{local_ip}:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
