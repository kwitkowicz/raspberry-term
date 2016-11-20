import threading
import time
import datetime
import random
import sqlite3
import math
import Adafruit_DHT

class TempLogger(threading.Thread):
    isRunning = True

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, interval = 5, in_memory_db = True):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=verbose)
        self.conn = None
        self.in_memory_db = in_memory_db
        self.last_measurement = None
        self.interval = interval
        self._setup()

    def _setup(self):
        #self.sensor
        self.start_db()

    def run(self):
        """
ProgrammingError: SQLite objects created in a thread can only be used in that same thread.The object was created in thread id 10052 and this is thread id 4532
"""
        while self.isRunning:
            self._make_measurement()
            time.sleep(self.interval)

    def stop(self):
        self.isRunning = False
        self.join()
        self.stop_db()

    def calc_dew_point(self,t,h):
        return math.pow((h/100.0),(1.0/8)) * (112 + (0.9 * t)) + (0.1 * t) - 112

    def _make_measurement(self,sensor=Adafruit_DHT.DHT11,pin=4):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        humidity,temp =  Adafruit_DHT.read_retry(sensor,pin)
        dew_point = float("{0:.2f}".format(self.calc_dew_point(temp,humidity)))
        self.last_measurement = [humidity,temp,dew_point]
        print(self.last_measurement)
        cur = self.conn.cursor()
        cur.execute("Insert into sensor_data(created_at, humidity, temperature, dew_point) values(?,?,?,?)",(now,humidity,temp,dew_point))
        print "taken at {0}\nhumidity: {1}\ntemperature: {2}\ndew_point: {3}".format(now,humidity,temp,dew_point)

    def get_last_measurement(self):
        if len(self.last_measurement) == 4:
            self.last_measurement[0]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.last_measurement.insert(0,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print "return last {}".format(self.last_measurement,)
        return self.last_measurement
    
    def get_last_n_rows(self, limit = 10):
        cur = self.conn.cursor()
        cur.execute("""select created_at, humidity, temperature from sensor_data order by created_at DESC limit ? """,(limit,))
        result = []
        while True:
            row = cur.fetchone()
            if row == None:
                break

            print row
            print type(row)

            result.append(row)
        return result

    def get_archival_data(self,date_from, date_to):
        cur = self.conn.cursor()
        if date_to is None:
            print "to is none"
            cur.execute("select created_at, humidity, temperature, dew_point from sensor_data WHERE created_at > ? order by created_at DESC",(date_from,)) 
        else:
            print "to is not none"
            cur.execute("select created_at, humidity, temperature, dew_point from sensor_data WHERE created_at > ? AND created_at < ? order by created_at DESC",
                    (date_from,date_to)) 
        result = []
        while True:
            row = cur.fetchone()
            if row == None:
                break
            result.append(row)
        return result
            
    def start_db(self):
        if self.in_memory_db:
            self.conn = sqlite3.connect(":memory:",check_same_thread=False)
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE sensor_data(id Integer Primary Key, created_at timestamp, humidity real, temperature real, dew_point real)")
            cur.close()
            self.conn.commit()
        else:
            self.conn = sqlite3.connect("logger.db",check_same_thread=False)
       
    def stop_db(self):
        """
        cur = self.conn.cursor()
        cur.execute("Select * from temp")
        while True:
            row = cur.fetchone()
            if row == None:
                break

            print row
        """
        self.get_last_n_rows()
        self.conn.close()

if __name__=='__main__':
    m = TempLogger() 
    m.start()
    time.sleep(5)
    m.stop()
