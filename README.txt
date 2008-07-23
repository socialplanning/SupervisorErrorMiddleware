A WSGI middleware which catches exceptions, formats them for supervisord
(http://www.supervisord.org), if you're running under supervisord, and
then re-raises them.

If you're using a pylons app, you can't just stick this into your
config as a filter, because the Pylons error handler will catch all
exceptions before they get here.
