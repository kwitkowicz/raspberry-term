import cherrypy
import sys
from temp_logger import TempLogger


class TempServer(object):

    def __init__(self, in_memory_db=True):
        self.logger = TempLogger(in_memory_db=in_memory_db)

    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def historic(self, *args, **kwargs):
        return open('historic.html')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def plot(self):
        return self.logger.get_last_measurement()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_historical_data(self, start_date, stop_date):
        if stop_date == '' or stop_date == 'null':
            stop_date = None
        if start_date == '' or start_date == 'null':
            start_date = None
        return self.logger.get_archival_data(start_date, stop_date)

    def run_background_task(self):
        self.logger.start()

    def stop_background_task(self):
        self.logger.stop()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-f':
        in_memory = False
    else:
        in_memory = True
    global_config = {
            'global': {
                'server.socket_host': '0.0.0.0',
                'server.socket_port': 8080,
                'log.screen': True,
                'engine.autoreload.on': False,
                'engine.SIGHUP': None,
                'engine.SIGTERM': None
            }
            }
    server = TempServer(in_memory_db=in_memory)
    print 'Server is running.'
    cherrypy.engine.subscribe('start', server.run_background_task)
    cherrypy.engine.subscribe('stop', server.stop_background_task)
    cherrypy.quickstart(server, '/', global_config)
