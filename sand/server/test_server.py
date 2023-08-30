import http.server
import socketserver


def simple_handler(site):
    class SimpleSiteServer(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=site.output_root, **kwargs)

    return SimpleSiteServer

class Servers:
    def __init__(self):
        self.BASE_PORT = 9000
        self.servers = {}

    def for_sites(self, sites):
        port = self.BASE_PORT
        for site in sites:
            server = socketserver.TCPServer(("", port), simple_handler(site))
            self.servers[port] = server
            print("Serving site %s at localhost:%d" % (site.root, port))
            server.serve_forever()
            port += 1
