''' stutter.test.test_buffered_logger module
    Created by photofroggy.
    This module contains the unit tests for the BufferedLogger object
    found in stutter.logging.
'''

import sys
import unittest

# stutter imports
from stutter.logging import BufferedLogger


class TestBufferedLogger(unittest.TestCase):
    
    def dummy(self, *args, **kwargs):
        """ Dummy method used in place of `stdout.write`. """
        self.called = True
    
    def setUp(self):
        self.called = False
        self.logger = BufferedLogger(stdout=self.dummy)
        self.logger._save = self.dummy
    
    def test_unbuffered(self):
        """ Test if the logger queues items instead of saving straight off the bat. """
        self.logger.message('Testing.')
        self.assertFalse(self.logger.queue.empty(),
            'BufferedLogger saved message unexpectedly')
    
    def test_buffered(self):
        """ Test if the logger pushes the queue when we tell it to. """
        self.logger.message('Testing')
        self.called = False
        self.logger.push()
        self.assertTrue(self.logger.queue.empty(),
            'BaseLogger did not try to save our messages on `push`')
    
    def test_flush(self):
        """ Test that `push` is capable of flushing the entire queue. """
        self.logger.message('Testing')
        self.logger.message('Testing')
        self.logger.message('Testing')
        self.logger.message('Testing')
        self.logger.message('Testing')
        self.logger.message('Testing')
        self.logger.message('Testing')
        self.logger.message('Testing')
        self.logger.message('Testing')
        
        self.logger.push(limit=1)
        self.assertFalse(self.logger.queue.empty(),
            '`push(limit=1)` flushed the entire queue')
        
        self.logger.push(limit=0)
        self.assertTrue(self.logger.queue.empty(),
            '`push(limit=0)` failed to flush queue')


# EOF
