import cherrypy
import os
from webapp.controller import TempServer, Config


class Server(object):

    def __init__(self):
        self.base_dir = os.path.normpath(os.path.abspath(os.path.curdir))
        self.configuration_path = os.path.join(self.base_dir, 'configuration')
        self.logs_dir = os.path = os.path.join(self.base_dir, 'logs')
        if not os.path.exists(self.logs_dir):
            os.mkdir(self.logs_dir)

        cherrypy.config.update(os.path.join(self.configuration_path, "server.cfg"))

    def run(self, in_memory=True):
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
        cfg_config = {
                '/': {
                    # the api uses restful method
                    # dispatching
                    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),

                    # all api calls require that the
                    # client passes HTTP basic authentication

                }

        }

        server = TempServer(in_memory_db=in_memory)
        print 'Server is running.'
        cherrypy.engine.subscribe('start', server.run_background_task)
        cherrypy.engine.subscribe('stop', server.stop_background_task)
        cherrypy.tree.mount(server, '/', config=global_config)
        cherrypy.tree.mount(Config(), '/config', config=global_config)
        cherrypy.config.update({'server.socket_host': '0.0.0.0', })
        cherrypy.config.update({'server.socket_port': 8080, })
        cherrypy.quickstart(server, '/', global_config)

if __name__ == '__main__':
    s = Server()
    s.run()
