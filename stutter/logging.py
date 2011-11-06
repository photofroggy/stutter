''' stutter.logging module
    Created by photofroggy
    Copyright (c) photofroggy 2011
'''

import os
import sys
import time
import os.path
from Queue import Queue
from threading import Thread


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
    
    def _fname(self, timestamp):
        """ Return a file name based on the given input. """
        return '{0}/{1}.txt'.format(self.save_folder, time.strftime('%Y-%m-%d', time.localtime(timestamp)))
    
    def get_level(self):
        """ Return the current log level of the logger. """
        return self.level
    
    def set_level(self, level):
        """ Set the current log level of the logger. """
        self.level = level
    
    def time(self, timestamp=None):
        """ Return the time formatted according to `stamp`. """
        return time.strftime(self.stamp, time.localtime(timestamp))
    
    def display(self, level, message, timestamp=None, **kwargs):
        """ Display the message on the screen. """
        msg = '{0}{1}\n'.format(self.time(timestamp), message)
        
        if self.get_level() <= level:
            self.stdout(msg)
        
        self.save(message, timestamp)
    
    def error(self, message, timestamp=None, **kwargs):
        """ Display an error message. """
        self.display(LEVEL.ERROR,
            'ERROR| {0}'.format(message),
            timestamp or time.time(),
            **kwargs
        )
    
    def warning(self, message, timestamp=None, **kwargs):
        """ Display a warning. """
        self.display(LEVEL.WARNING,
            'WARNING| {0}'.format(message),
            timestamp or time.time(),
            **kwargs
        )
    
    def message(self, message, timestamp=None, **kwargs):
        """ Display a message. """
        self.display(LEVEL.MESSAGE,
            ' {0}'.format(message),
            timestamp or time.time(),
            **kwargs
        )
    
    def debug(self, message, timestamp=None, **kwargs):
        """ Display a debug message. """
        self.display(LEVEL.DEBUG,
            'DEBUG| {0}'.format(message),
            timestamp or time.time(),
            **kwargs
        )
    
    def save(self, message, timestamp=None):
        """ Save the given message to a log file. """
        if not self.save_logs or not self.save_folder:
            return
        
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder, 0o755)
        
        with open(self._fname(timestamp), 'a') as file:
            file.write('{0}{1}\n'.format(self.time(timestamp), message))


class BufferedLogger(BaseLogger):
    """ Buffered logger.
        
        This logging class does not instantly save messages. Instead, messages
        are placed in a queue, and only saved when the `push` method is called.
        
        Typically, no programs should use this class unless greater control is
        needed when saving messages.
    """
    
    queue = None
    
    def __init__(self, *args, **kwargs):
        BaseLogger.__init__(self, *args, **kwargs)
        self.queue = Queue()
    
    def _display(self, lower, message, timestamp, **kwargs):
        """ Display the message. """
        if lower:
            return
        
        self.stdout('{0}{1}\n'.format(self.time(timestamp), message))
    
    def _save(self, fname, chunk):
        """ Save multiple log messages to a single file. """
        with open(fname, 'a') as file:
            for data in chunk:
                file.write('{0}{1}\n'.format(self.time(data[3]), data[2]))
    
    def display(self, level, message, timestamp=None, **kwargs):
        """ Buffered display method. """
        data = (self.get_level(), level, message, timestamp or time.time(), kwargs)
        self._display(data[0] > data[1], data[2], data[3], **data[4])
        self.queue.put(data)
    
    def push(self, limit=5):
        """ Push some queued items out of the queue.
            
            This method causes queued items to be written to be saved to a file.
            
            Only `limit` items will be pushed out of the queue. If `limit` is
            `0`, then all items will be pushed from the queue.
        """
        if limit < 0:
            return
        
        if self.queue.empty():
            return
        
        sdata = {}
        iter = 0
        
        # First we sort the data we want into lists of messages that will be
        # saved in the same file. This way we don't have to keep opening and
        # closing files.
        while not self.queue.empty():
            item = self.queue.get()
            fname = self._fname(item[3])
            
            try:
                sdata[fname].append(item)
            except KeyError:
                sdata[fname] = []
                sdata[fname].append(item)
            
            if limit > iter+1:
                iter+= 1
                continue
            
            break
        
        # The following two lines make the above loop pointless save for the
        # purpose of syphoning the queue.
        if not self.save_logs:
            return
        
        for fname in sdata:
            self._save(fname, sdata[fname])


# EOF
