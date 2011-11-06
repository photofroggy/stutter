''' stutter.logging module
    Created by photofroggy
    Copyright (c) photofroggy 2011
'''

import os
import sys
import time
import os.path
from Queue import Queue


class LEVEL:
    """ Determines the logging levels available in the package. """
    DEBUG = 0
    MESSAGE = 1
    WARNING = 2
    ERROR = 3


class BaseLogger(object):
    """ Basic class used for logging. No buffering or threading is used
        in this class.
    """
    
    level = LEVEL.MESSAGE
    save_logs = True
    save_folder = None
    stamp = None
    
    
    def __init__(self, stdout=None, stamp=None, level=None, save_folder=None, save_logs=True):
        
        if stdout is None:
            def default_write(msg=''):
                sys.stdout.write(msg)
                sys.stdout.flush()
            self.stdout = default_write
        else:
            self.stdout = stdout
        
        self.save_logs = save_logs
        
        if level is not None:
            self.level = level
        
        self.save_folder = save_folder or './log'
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder, 0o755)
        
        self.stamp = stamp or '%H:%M:%S|'
    
    def get_level(self):
        """ Return the current log level of the logger. """
        return self.level
    
    def set_level(self, level):
        """ Set the current log level of the logger. """
        self.level = level
    
    def time(self, timestamp=None):
        """ Return the time formatted according to `stamp`. """
        return time.strftime(self.stamp, time.localtime(timestamp))
    
    def display(self, message, timestamp=None):
        """ Display the message on the screen. """
        out = '{0}{1}\n'.format(self.time(timestamp), message)
        self.stdout(out)
        return len(out)
    
    def error(self, message, timestamp=None):
        """ Display an error message. """
        timestamp = timestamp or time.time()
        message = 'ERROR| {0}'.format(message)
        self.save(message, timestamp)
        
        if self.level <= LEVEL.ERROR:
            return self.display(message, timestamp)
        
        return 0
    
    def warning(self, message, timestamp=None):
        """ Display a warning. """
        timestamp = timestamp or time.time()
        message = 'WARNING| {0}'.format(message)
        self.save(message, timestamp)
        
        if self.level <= LEVEL.WARNING:
            return self.display(message, timestamp)
        
        return 0
    
    def message(self, message, timestamp=None):
        """ Display a message. """
        timestamp = timestamp or time.time()
        message = ' {0}'.format(message)
        self.save(message, timestamp)
        
        if self.level <= LEVEL.MESSAGE:
            return self.display(message, timestamp)
        
        return 0
    
    def debug(self, message, timestamp=None):
        """ Display a debug message. """
        timestamp = timestamp or time.time()
        message = 'DEBUG| {0}'.format(message)
        self.save(message, timestamp)
        
        if self.level <= LEVEL.DEBUG:
            return self.display(message, timestamp)
        
        return 0
    
    def save(self, message, timestamp=None):
        """ Save the given message to a log file. """
        if not self.save_logs or not self.save_folder:
            return
        
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder, 0o755)
            
        fname = '{0}/{1}.txt'.format(self.save_folder, time.strftime('%Y-%m-%d', time.localtime(timestamp)))
        
        with open(fname, 'a') as file:
            file.write('{0}{1}\n'.format(self.time(timestamp), message))



# EOF
