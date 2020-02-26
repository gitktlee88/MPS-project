import MySQLdb
# import logging
import os

class MySQLDBcon:
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

    def connect(self, dbname):
        try:
            self.connector = MySQLdb.connect(host=self.host,
                                            user=self.user,
                                            passwd=self.pw,
                                            charset=self.char,)
        except Exception as e:
            print(e)


    """   fetchall(),
      the return value is a sequence of "tuples" that contain
      the "row values".
    """
    def query_db(self, sql_cmd, db_use = ''):
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
            return r

    def __del__(self):
        print('db close')
        self.connector.close()
