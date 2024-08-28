import http.server
import socketserver
import threading
from time import sleep


def simple_handler(site):
    class SimpleSiteServer(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=site.output_root, **kwargs)

    return SimpleSiteServer


class Server(threading.Thread):
    def __init__(self, stop_event, site, port, *args, **kwargs):
        super().__init__(daemon=True, name="Server %d" % port, *args, **kwargs)
        self.stop_event = stop_event
        self.site = site
        self.port = port
        self.server = None

    def run(self):
        server = socketserver.TCPServer(('', self.port), simple_handler(self.site))
        with server:
            self.server = threading.Thread(target=server.serve_forever)
            self.server.daemon = True
            self.server.start()

            print("Serving site %s at localhost:%d" % (self.site.root, self.port))

            while not self.stop_event.is_set():
                sleep(5)

            print("Site %s at localhost:%d shutting down..." % (self.site.root, self.port))
            server.shutdown()
            self.server.join()


class Servers:
    def __init__(self, port=9000):
        self.BASE_PORT = port
        self.servers = {}

    def stop_servers(self, stop_event):
        print("Stopping servers...")
        stop_event.set()
        for server in self.servers.values():
            server.join()

    def for_sites(self, sites):
        stop_event = threading.Event()

        port = self.BASE_PORT
        for site in sites:
            server_thread = Server(stop_event, site, port)
            self.servers[port] = server_thread
            server_thread.start()
            port += 1

        while True:
            try:
                sleep(5)
            except KeyboardInterrupt:
                self.stop_servers(stop_event)
                break
