#!/usr/bin/env python3
"""
Simple Message Queue

It receives a queue name and any message string
on `/push/<queue-name>` POST endpoint and
puts the message in the queue with the received name,
creating one if does not exist, and receives
a queue name on `/pull/<queue-name>` GET endpoint and
returns the oldest message in the queue with
the received name, empty response if queue is empty or
404 if queue does not exist.

Usage::
    ./main.py [<port>]
"""
import logging
from queue import SimpleQueue, Empty
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

queues = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code):
        self.send_response(status_code)
        self.end_headers()

    def do_POST(self):
        path, queue_name = self.path.split('/', 2)[1:]
        if path == 'push':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            if queue_name not in queues:
                queues[queue_name] = SimpleQueue()
            queues[queue_name].put(post_data)
            self._set_response(200)
        else:
            self._set_response(404)

    def do_GET(self):
        path, queue_name = self.path.split('/', 2)[1:]
        if path == 'pull' and queue_name in queues:
            try:
                result = queues[queue_name].get(block=False)
                self._set_response(200)
                self.wfile.write(result)
            except Empty:
                self._set_response(204)
        else:
            self._set_response(404)


def run(server_class=ThreadingHTTPServer, handler_class=HTTPRequestHandler, port=8001):
    logging.basicConfig(level=logging.INFO)
    with server_class(('', port), handler_class) as httpd:
        logging.info("Server running on port %d..." % port)
        httpd.serve_forever()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
