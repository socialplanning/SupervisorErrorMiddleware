import os
import traceback
from paste.request import construct_url
from pprint import pformat

class SupervisorErrorMiddleware_:
    def __init__(self, app, app_conf=None):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except:
            environ = environ.copy()
            tb = traceback.format_exc()
            try:
                url = construct_url(environ)
            except:
                url = "Error getting URL from environ"
            try:
                method = environ['REQUEST_METHOD']
            except:
                method = "No HTTP method in WSGI request"

            print """<!--XSUPERVISOR:BEGIN-->
Content-Type: text/plain
Request-url: %s
Method: %s

Environment: %s


Traceback: %s
<!--XSUPERVISOR:END-->""" % (url,
                             method,
                             pformat(environ),
                             tb)
            raise


def SupervisorErrorMiddleware(app, app_conf=None):
    if not 'SUPERVISOR_ENABLED' in os.environ:
        return app
    else:
        return SupervisorErrorMiddleware_(app, app_conf)

