"""DB function helper"""
import cymysql as mdb
import sys

class DBhelper(object):
    """Class that simplifies adding raditation datapoints to MySQL database.
    """
    def __init__(self, host, username, pw, db):
        self._host = host
        self._username = username
        self._pw = pw
        self._db = db
        self._con = None
        self._cur = None

    def __enter__(self):
        self._con = mdb.connect(self._host, self._username, self._pw, self._db)
        self._cur = self._con.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        if self._con:
            self._con.close()

    def get_version(self):
        '''Prints database version'''
        self._cur.execute("SELECT VERSION()")
        ver = self._cur.fetchone()
        print "Database version : %s " % ver

    def add_data(self):
        '''add radiation datapoint to database'''
        pass


def main():
    '''Runs if called as main program'''
    try:
        with DBhelper('localhost', 'Rad_DB_py', '12345678', 'RadDB') as rdb:
            rdb.get_version()


    except mdb.Error as err:
        print "Error %d: %s" % (err.args[0], err.args[1])
        sys.exit(1)



if __name__ == '__main__':
    sys.exit(main())
