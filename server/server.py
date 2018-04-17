from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import logging
import json
from sys import argv, stdout, stderr
from ast import literal_eval
import numpy as np


logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
mylogger = logging.getLogger()
mylogger.setLevel(logging.INFO)

logPath = "./"
fileName = 'server'
fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.INFO)
mylogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)
mylogger.addHandler(consoleHandler)

errHandler = logging.StreamHandler(stderr)
errHandler.setFormatter(logFormatter)
errHandler.setLevel(logging.ERROR)
mylogger.addHandler(errHandler)


def handle(data_json):
    array_data = literal_eval(data_json['pic'])
    print(type(array_data))
    print(np.asarray(array_data).shape)
    if np.asarray(array_data).shape != (224,224,3):
        return False 
    else:
        return True


class S(BaseHTTPRequestHandler):
    def _set_response(self, result):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        msg = {"reply":result}
        self.wfile.write(json.dumps(msg).encode('utf-8'))
        return

    def do_GET(self):
        mylogger.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        print("length", content_length)
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        mylogger.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        data_json = json.loads(post_data.decode('utf-8'))
        if handle(data_json):

            self._set_response("good")
        else:
            self._set_response("bad")
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """handle requests in a separate thread."""

def run(handler_class=S, port=8000):

    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, handler_class)
    mylogger.info('Starting httpd...on ' + str(port) + "\n" )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    mylogger.info('Stopping httpd...\n')

def startServer():

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

startServer()

