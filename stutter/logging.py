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
    """ Basic class used for logging.
        
        No buffering or threading is used in this class. Output messages given
        to the different methods are instantly given to the provided output
        method and saved to a log file in the desired log folder.
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
    
    def display(self, level, message, timestamp=None):
        """ Display the message on the screen. """
        msg = '{0}{1}\n'.format(self.time(timestamp), message)
        
        if self.level <= level:
            self.stdout(msg)
        
        self.save(message, timestamp)
    
    def error(self, message, timestamp=None):
        """ Display an error message. """
        timestamp = timestamp or time.time()
        message = 'ERROR| {0}'.format(message)
        self.display(LEVEL.ERROR, message, timestamp)
    
    def warning(self, message, timestamp=None):
        """ Display a warning. """
        timestamp = timestamp or time.time()
        message = 'WARNING| {0}'.format(message)
        self.display(LEVEL.WARNING, message, timestamp)
    
    def message(self, message, timestamp=None):
        """ Display a message. """
        timestamp = timestamp or time.time()
        message = ' {0}'.format(message)
        self.display(LEVEL.MESSAGE, message, timestamp)
    
    def debug(self, message, timestamp=None):
        """ Display a debug message. """
        timestamp = timestamp or time.time()
        message = 'DEBUG| {0}'.format(message)
        self.display(LEVEL.DEBUG, message, timestamp)
    
    def save(self, message, timestamp=None):
        """ Save the given message to a log file. """
        if not self.save_logs or not self.save_folder:
            return
        
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder, 0o755)
            
        fname = '{0}/{1}.txt'.format(self.save_folder, time.strftime('%Y-%m-%d', time.localtime(timestamp)))
        
        with open(fname, 'a') as file:
            file.write('{0}{1}\n'.format(self.time(timestamp), message))


class BufferedLogger(BaseLogger):
    """ Buffered logger.
        
        This logging class does not instantly display and save messages.
        Instead, messages are placed in a queue, and only displayed and saved
        when the `push` method is called.
        
        Typically, no programs should use this class unless greater control is
        needed when displaying and saving messages.
    """
    
    def push(self, limit=5):
        """ Push some queued items out of the queue.
            
            This method causes queued items to be written to the given display
            method, and to be saved to a file.
            
            Only `limit` items will be pushed out of the queue. If `limit` is
            `0`, then all items will be pushed from the queue.
        """
        pass


# EOF
