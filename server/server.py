"""
server.py

Author: Xenon

A basic HTTP server, which as of now is capable of handling HEAD, POST,
and GET requests. On running this file, an http server is created on the
specified host, where it listens for requests.

Classes:
 - Server :: Inherits BaseHTTPRequestHandler : A basic http server.

"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from server.database.db import Database
import dotenv
import json
import sys
import os

dotenv.load_dotenv()

class Server(BaseHTTPRequestHandler):
    port = int(os.getenv('PORT'))
    # TODO - update to use database @./database/db.py
    jsonPath = os.getenv('SERVER_JSONPATH')  # The path which the server's primary JSON file is located.
    database = Database()

    def _set_headers(self, _status=200) -> None:
        """Sets the response headers for the request.

        Parameters:
         - _status :: int - default 200 : The status code of the request.

        Returns :: None
        """
        self.send_response(_status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self) -> None:
        """Handles HEAD requests. This needs to be expanded upon,
        so will likely see a complete overhaul *soon(tm)*.

        Responses:
         - 200 :: success : Everything went smoothly.

        Returns :: None
        """
        self._set_headers()

    def do_GET(self) -> None:
        """Handles GET requests. It should be sent json database in the header
        which contains the ID of the content to be read from the master
        json file.

        Responses:
         - 200 :: success : Everything went smoothly.
         - 400 :: failure : The database sent was not json.
         - 422 :: failure : Invalid key - missing ID.

        Returns :: None
        """
        # E#nsure that the sent database type is actually json.
        if self.headers['Content-Type'] != 'application/json':
            self._set_headers(400)
            return

        try:
            # Get the sent content from within the header.
            length = int(self.headers['Content-Length'])
            msg = json.loads(self.rfile.read(length))

            id = msg['id']
            if id < 0:
                self._set_headers(400)  # If it's negative, throw an error.
                return False

            # Otherwise, read the desired content
            try:
                data = self.database.READ(id)
                data['interactions'] += 1  # Increment User Interactions (placeholder)
                # The wfile is actually the response content, which makes
                # sense when you consider that that's the HTML that the
                # browser will end up rendering.
            except KeyError:
                data = {'interactions': 1}  # If the ID doesn't exist, create a new entry.

            self._set_headers()
            self.wfile.write(bytes(
                json.dumps(data),  # Query the database.
                "utf-8"
            ))

        except KeyError:
            # If the master JSON file is not found, throw an error.
            self._set_headers(422)

    def do_POST(self) -> None:
        """Handles POST requests. It should be sent json database in the header
        which contains the ID of the content to be updated, along with
        the database to update(though this functionality has yet to be added).

        Responses:
         - 200 :: success : Everything went smoothly.
         - 400 :: failure : The content type of the header was not json,
                            or the provided ID was sub-zero
         - 404 :: failure : The server was unable to find the master json file.
         - 422 :: failure : The provided header did not contain a content ID.

        Returns :: None
        """
        # Make sure that the sent database type is actually json.
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

            self._set_headers()

        except FileNotFoundError:
            # If master JSON file is not found, throw an error.
            self._set_headers(404)

    def _process_Json(self, msg: dict) -> bool:
        """Processes the json database sent in a POST request.

        Parameters:
         - msg :: dict : The database sent in the header of a POST request.

        Returns :: bool : Was successful? If so, return True.
        """
        try:
            # Attempt to grab the 'user' ID from the header
            id = msg['id']
            if id < 0:
                self._set_headers(400)  # If it's negative, throw an error.
                return False

            # Otherwise, update the master json file.
            try:
                db_content = self.database.READ(id)
                db_content['interactions'] += 1  # Increment User Interactions (placeholder)
            except KeyError:
                db_content = {'interactions': 1}  # If the ID doesn't exist, create a new entry.

            self.database.WRITE(id, db_content)

        except KeyError:
            # If the ID isn't found, throw an error.
            self._set_headers(422)
            return False

        return True  # Nominal exit.

if __name__ == '__main__':
    httpd = HTTPServer(('localhost', Server.port), Server)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)  # Silent exit on ^C.
