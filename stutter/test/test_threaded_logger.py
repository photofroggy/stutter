''' stutter.test.test_threaded_logger module
    Created by photofroggy.
    This module contains the unit tests for the ThreadedLogger object
    found in stutter.logging.
'''

import sys
import unittest

# stutter imports
from stutter.logging import ThreadedLogger


class TestThreadedLogger(unittest.TestCase):
    
    def dummy(self, *args, **kwargs):
        """ Dummy method used in place of `stdout.write`. """
        self.called = True
    
    def setUp(self):
        self.called = False
        self.logger = ThreadedLogger(self.dummy)
    
    def test_threading(self):
        """ Test if the logger queues items instead of saving straight off the bat. """
        self.logger.start()
        
        self.assertTrue(self.logger.is_running(),
            '`start` method did not start a thread')
        
        self.logger.stop()
        self.logger.join(3)
        
        self.assertFalse(self.logger.is_running(),
            '`stop` method did not stop the thread in time')


# EOF
