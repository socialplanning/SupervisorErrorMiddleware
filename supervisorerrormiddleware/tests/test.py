from supervisorerrormiddleware import SupervisorErrorMiddleware
import os
import sys
import paste.fixture

class DummyOutput:
    def __init__(self):
        self._buffer = []

    def write(self, data):
        self._buffer.append(data)

    def flush(self):
        self._buffer = []

def bad_app(environ, start_response):
    if environ['PATH_INFO'] != '/good':
        raise Exception("Bad Kitty")
    else:
        start_response("200 OK", [('Content-type', 'text/html')])
        return ["Good Kitty"]

def test_without_supervisor():
    old_stdout = sys.stdout
    try:
        sys.stdout = DummyOutput()

        app = bad_app
        app = SupervisorErrorMiddleware(app)
        app = paste.fixture.TestApp(app)
        failed = False
        try:
            app.get("/")
        except:
            failed = True
        assert failed
        output = "".join(sys.stdout._buffer)
        sys.stdout.flush()
        assert not "Bad Kitty" in output
        assert not "GET" in output
        response = app.get("/good")
        output = "".join(sys.stdout._buffer)
        sys.stdout.flush()
        response.mustcontain("Good Kitty")
        assert not "Bad Kitty" in output
        assert not "GET" in output


    finally:
        sys.stdout = old_stdout

def test_with_supervisor():

    #Why is there output when stdout is redirected?  Because
    #paste.fixture.TestApp gets around the redirection.
    old_stdout = sys.stdout
    try:
        os.environ['SUPERVISOR_ENABLED'] = "1" #fake supervisor
        sys.stdout = DummyOutput()

        app = bad_app
        app = SupervisorErrorMiddleware(app)
        app = paste.fixture.TestApp(app)
        failed = False
        try:
            app.get("/")
        except:
            failed = True
        assert failed
        output = "".join(sys.stdout._buffer)
        sys.stdout.flush()
        assert "Bad Kitty" in output
        assert "GET" in output
        response = app.get("/good")
        output = "".join(sys.stdout._buffer)
        sys.stdout.flush()
        response.mustcontain("Good Kitty")
        assert not "Bad Kitty" in output
        assert not "GET" in output

    finally:
        sys.stdout = old_stdout
        del os.environ['SUPERVISOR_ENABLED']

