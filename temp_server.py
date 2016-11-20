
import cherrypy
import threading
import time
from temp_logger import TempLogger

class TempServer(object):

    def __init__(self):
        self.logger = TempLogger()

    @cherrypy.expose
    def index(self):
        return open ('index.html')

    @cherrypy.expose
    def historic(self):
        return open ('historic.html')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def plot(self):
        return self.logger.get_last_measurement()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_historical_data(self,start_date,stop_date):
        if stop_date =='':
            stop_date=None 
        return self.logger.get_archival_data(start_date,stop_date)

    def run_background_task(self):
        self.logger.start()
    
    def stop_background_task(self):
        self.logger.stop()

if __name__ == '__main__':
    global_config = {
            'global':{
                'server.socket_host': '0.0.0.0',
                'server.socket_port': 8080,
                'log.screen': True,
                'engine.autoreload.on': False,
                'engine.SIGHUP': None,
                'engine.SIGTERM': None
    } 
            }
    server = TempServer()
    print 'Server is running.'
    cherrypy.engine.subscribe('start',server.run_background_task)
    cherrypy.engine.subscribe('stop',server.stop_background_task)
    cherrypy.quickstart(server, '/', global_config)
