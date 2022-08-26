"""
db.py

Author: Xenon

A Simple database which can store database in many small JSON files. It is
fairly unoptimized as of now, so performance is likely to be less than
ideal, however, the eventual goal is to be able to handle decent quantities
of database, with speeds of under 500ms.

Classes:
 - Database :: Inherits object : A simple database.

"""

from helpers.util import *

class Database:
    MASTER_JSON = "server/database/master.json"

    # Process the contents of master.json.
    # Respond to request(s) for database by:
    #  - Loading required JSON file (this should be figured out in DB)
    #  - Grabbing requested database from the file
    #  - Returning the database.
    #
    # Planned features:
    #  - Breaking databases into many little JSON files, instead of
    #    loading a single massive dictionary into RAM.

    def READ(self, id: int) -> dict:
        """Reads the contents of the database at ID id.

        Parameters:
         - id :: int : The id to read at from the database.

        Returns :: dict : The value at ID id
        """
        return read_json(self.MASTER_JSON)[str(id)]

    def WRITE(self, id: int, data: dict) -> None:
        """Writes to the database at id, witht the data passed

        Parameters:
         - id :: int : The id to write to from the database.
         - data :: dict : The data to write.

        Returns :: None
        """
        database = read_json(self.MASTER_JSON)
        database[str(id)] = data
        write_json(self.MASTER_JSON, database)
