"""
server.py

Author: Xenon

A basic HTTP server, which as of now is capable of handling HEAD, POST,
and GET requests. On running this file, an http server is created on the
specified host, where it listens for requests.

Classes:
 - Server :: Inherits BaseHTTPRequestHandler : A basic http server.

Functions:
 - write_json :: None : Writes data into a json file.
 - read_json :: dict : Reads data from a specified json file.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import dotenv
import json
import os

dotenv.load_dotenv()

def write_json(filepath: str, data: dict):
    """Writes data into the json file
    specified with the filepath parameter.

    Parameters:
     - filepath :: str : The file to be written to.
     - data :: dict : The data to be written into the file.

    Returns :: None
    """
    with open(filepath, 'w', encoding='UTF-8') as f:
        f.write(json.dumps(data))

def read_json(filepath) -> dict:
    """Reads the data from the json file
    specified by filepath.

    Parameters:
     - filepath :: str : The file to be read from.

    Returns :: dict : The contents of the json file.
    """
    with open(filepath, 'r', encoding='UTF-8') as f:
        return json.loads(f.read())

class Server(BaseHTTPRequestHandler):
    port = int(os.getenv('PORT'))
    jsonPath = os.getenv('SERVER_JSONPATH')  # The path which the server's primary JSON file is located.

    def _set_headers(self, _status=200):
        """Sets the response headers for the request.

        Parameters:
         - _status :: int - default 200 : The status code of the request.

        Returns :: None
        """
        self.send_response(_status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        """Handles HEAD requests. This needs to be expanded upon,
        so will likely see a complete overhaul *soon(tm)*.

        Responses:
         - 200 :: success : Everything went smoothly.

        Returns :: None
        """
        self._set_headers()

    def do_GET(self):
        """Handles GET requests. It should be sent json data in the header
        which contains the ID of the content to be read from the master
        json file.

        Responses:
         - 200 :: success : Everything went smoothly.
         - 400 :: failure : The data sent was not json.
         - 404 :: failure : The server was unable to find the master json file,.

        Returns :: None
        """
        # Make sure that the sent data type is actually json.
        if self.headers['Content-Type'] != 'application/json':
            self._set_headers(400)
            return

        try:
            file = json.load(open(self.jsonPath))

            # Get the sent content from within the header.
            length = int(self.headers['Content-Length'])
            msg = json.loads(self.rfile.read(length))

            self._set_headers()
            # The wfile, as it turns out, is actually the
            # response. who would've guessed?
            self.wfile.write(bytes(json.dumps(file[str(msg['id'])]), "utf-8"))

        except FileNotFoundError:
            # If the master JSON file is not found, throw an error.
            self._set_headers(404)

    def do_POST(self):
        """Handles POST requests. It should be sent json data in the header
        which contains the ID of the content to be updated, along with
        the data to update(though this functionality has yet to be added).

        Responses:
         - 200 :: success : Everything went smoothly.
         - 400 :: failure : The content type of the header was not json,
                            or the provided ID was sub-zero
         - 404 :: failure : The server was unable to find the master json file.
         - 422 :: failure : The provided header did not contain a content ID.

        Returns :: None
        """
        # Make sure that the sent data type is actually json.
        if self.headers['Content-Type'] != 'application/json':
            self._set_headers(400)
            return

        try:
            # Try to read the contents of the header.
            length = int(self.headers['Content-Length'])
            msg = json.loads(self.rfile.read(length))

            # Process the json sent, and check if it's an error.
            process_error = self._process_Json(msg)
            if not process_error: return

        except FileNotFoundError:
            # If master JSON file is not found, throw an error.
            self._set_headers(404)
            return

        self._set_headers()

    def _process_Json(self, msg: dict) -> bool:
        """Processes the json data sent in a POST request.

        Parameters:
         - msg :: dict : The data sent in the header of a POST request.

        Returns :: bool : Was successful? If so, return True.
        """
        try:
            # Attempt to grab the 'user' ID from the header
            id = msg['id']
            if id < 0:
                self._set_headers(400) # If it's negative, throw an error.
                return False

            # Otherwise, update the master json file.
            file = read_json(self.jsonPath)
            try:
                file[str(id)]['interactions'] += 1  # Increment User Interactions (placeholder)
            except KeyError:
                file[str(id)] = {'interactions': 1}  # If the ID doesn't exist, create a new entry.
            write_json(self.jsonPath, file)  # Write to the file the new changes.

        except KeyError:
            # If the ID isn't found, throw an error.
            self._set_headers(422)
            return False

        return True  # Nominal exit.

if __name__ == '__main__':
    httpd = HTTPServer(('localhost', Server.port), Server)
    httpd.serve_forever()
