import MySQLdb
# import logging
import os


class MySQLdb_connection(object):
    """mysql db connection"""

    def __init__(self, connection_string=os.environ["CONN"], db=''):
        # connect(host, user, passwd, db)

        connection_string = connection_string + ',' + db

        vars = connection_string.split(',')
        self.host = vars[0]
        self.user = vars[1]
        self.pw = vars[2]
        self.char = "utf8mb4"
        # print(connection_string)
        self.connector = None

        try:
            self.connector = MySQLdb.connect(host=self.host,
                                             user=self.user,
                                             passwd=self.pw,
                                             charset=self.char,)
        except Exception as e:
            print(e)

    def __del__(self):
        self.connector.close()
        # print('__del__')

    """   fetchall(),
      the return value is a sequence of "tuples" that contain
      the "row values".
    """

    def query_db(self, sql_cmd, db_use=''):
        r = None
        try:
            cur = self.connector.cursor()
            r = cur.execute(sql_cmd)
            # print(sql_cmd)
            if r != 0:
                r = cur.fetchall()

            self.connector.commit()
        except Exception as e:
            print(e)
            self.connector.rollback()
        finally:
            cur.close()
            # self.connector.close()
            if r:
                return r


# executes when your script is called from the command-line
if __name__ == "__main__":
    print('How to use?\n'
          'MySQLdb_connection.query_db("your-sql-cmd")')
