class DbDriverInterface:
    def __init__(self, db_name, col_name):
        self._db_name = db_name
        self._col_name = col_name

