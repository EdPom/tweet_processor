import http.server
import socketserver
import memcache

class MyHttpHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Root - send index.html
            http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/stats.json':
            # Client is requesting status update
            # Return the values in memcache, in JSON
            self.send_response(200)
            baseball_count = getMemcachedItem('baseball_count')
            basketball_count = getMemcachedItem('basketball_count')
            response = bytes('{"baseball_count":' + str(baseball_count) + ',"basketball_count":'+ str(basketball_count) + '}', 'utf-8')
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-length', len(response))
            self.end_headers()
            self.wfile.write(response)
        else:
            # Refuse any other request
            self.send_response(403)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

PORT = 8000
Handler = MyHttpHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def getMemcachedItem(key):
    return mc.get(key)

print("serving at port", PORT)
httpd.serve_forever()
