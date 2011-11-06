''' stutter.test.test_buffered_logger module
    Created by photofroggy.
    This module contains the unit tests for the BufferedLogger object
    found in stutter.logging.
'''

import sys
import unittest

# stutter imports
from stutter.logging import LEVEL
from stutter.logging import BufferedLogger


class TestBufferedLogger(unittest.TestCase):
    
    def dummy(self, msg=''):
        """ Dummy method used in place of `stdout.write`. """
        self.called = True
    
    def setUp(self):
        self.called = False
        self.logger = BufferedLogger(self.dummy, save_logs=False)
    
    def test_unbuffered(self):
        """ Test if the logger queues items instead of printing straight off the bat. """
        self.logger.message('Testing.')
        self.assertFalse(self.called, 'BufferedLogger called given output method unexpectedly')
    
    def test_buffered(self):
        """ Test if the logger pushes the queue when we tell it to. """
        self.logger.message('Testing')
        self.logger.push()
        self.assertTrue(self.called, 'BaseLogger did not call the given output method')


# EOF
