import cherrypy
import json
from worker.temp_logger import TempLogger


class Config(object):

    @cherrypy.expose
    def index(self):
        return open('config.html')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_config(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
        return data

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def save_config(self):
        print 'in save config'
        input_json = cherrypy.request.json
        print input_json
        with open('config.json', 'w') as outfile:
                json.dump(input_json, outfile)
        return {"operation": "request", "result": "success"}


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
        print("run background task")
        self.logger.start()

    def stop_background_task(self):
        self.logger.stop()
