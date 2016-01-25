"""DB function helper"""
import cymysql as mdb
import sys
from datetime import datetime

class Helper(object):
    """Class that simplifies adding raditation datapoints to MySQL database.
    """
    def __init__(self, host, username, pw, db):
        self._host = host
        self._username = username
        self._pw = pw
        self._db = db
        #self._con = None
        #self._cur = None
        self._con = mdb.connect(self._host, self._username, self._pw, self._db, charset='utf8')
        self._cur = self._con.cursor()
        #print(self._con)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Close connection")
        if self._con:
            self._con.close()

    def get_version(self):
        '''Prints database version'''
        self._cur.execute('SELECT VERSION()')
        ver = self._cur.fetchone()
        print("Database version : %s " % ver)


    def add_data(self, fd_id, dist, value, cap_time=None):
        '''add radiation datapoint to database'''
        if(cap_time is None):
            cap_time = datetime.today()
        self._cur.execute("""INSERT INTO data (collect_time, upload_time, feed_id, rad_distance, value)
            VALUES (%s, %s, %s, %s, %s)""", (cap_time, datetime.today(), fd_id, dist, value))
        self._con.commit()


def main():
    '''Runs if called as main program'''
    try:
        with Helper('localhost', 'Rad_DB_py', '12345678', 'RadDB') as rdb:
            rdb.get_version()
            rdb.add_data('test_id', 6)


    except Exception as err:
        print "Error %d: %s" % (err.args[0], err.args[1])
        sys.exit(1)



if __name__ == '__main__':
    sys.exit(main())
