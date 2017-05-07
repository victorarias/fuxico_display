import cherrypy

import dateutil.parser
import datetime
from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class HelloWorld(object):
    def __init__(self):
        self.end_at = None
        self.timer = RepeatedTimer(1, console_output, self)

    @cherrypy.expose
    def start(self, str_end_at):
        self.end_at = dateutil.parser.parse(str_end_at)
        self.timer.start()

    @cherrypy.expose
    def stop(self):
        self.end_at = None
        self.timer.stop()

def console_output(context):
    if context.end_at == None:
        return

    if context.end_at < datetime.datetime.now():
        context.timer.stop()
        context.end_at = None

    if context.end_at == None:
        return

    diff = context.end_at - datetime.datetime.now()
    print(diff.total_seconds())

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
