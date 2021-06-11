import os
bind = '0.0.0.0:'+ str(os.environ.get('PORT'))
workers = 1
timeout = 120
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True