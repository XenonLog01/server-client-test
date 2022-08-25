from http.server import HTTPServer, BaseHTTPRequestHandler
import dotenv
import json
import os

dotenv.load_dotenv()


def write_json(file, data):
    with open(file, 'w', encoding='UTF-8') as f:
        f.write(json.dumps(data))

def read_json(file) -> dict:
    with open(file, 'r', encoding='UTF-8') as f:
        return json.loads(f.read())

class Server(BaseHTTPRequestHandler):
    port = int(os.getenv('PORT'))
    jsonPath = os.getenv('SERVER_JSONPATH')

    def _set_headers(self, _status=200, data=None):
        if data is not None:
            self.send_response(_status, data)
        else:
            self.send_response(_status)

        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        try:
            file_to_open = open(self.jsonPath)
            self.wfile.write(bytes(json.dumps(json.load(file_to_open)),
                                   "utf-8"))
        except FileNotFoundError:
            self._set_headers(404)

    def do_POST(self):
        if self.headers['Content-Type'] != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        try:
            length = int(self.headers['Content-Length'])
            msg = json.loads(self.rfile.read(length))

            process_error = self.process_Json(msg)

            if process_error:
                return

        except FileNotFoundError:
            self._set_headers(400)
            return

        self._set_headers()

    def process_Json(self, msg) -> bool:
        try:
            id = msg['id']
            if id < 0:
                self._set_headers(400)
                return True

            file = read_json(self.jsonPath)
            file[str(id)]['interactions'] += 1
            write_json(self.jsonPath, file)

        except KeyError:
            self._set_headers(422)
            return True

        return False

httpd = HTTPServer(('localhost', Server.port), Server)
httpd.serve_forever()
