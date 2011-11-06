''' stutter.test.test_basic_logger module
    Created by photofroggy.
    This module contains the unit tests for the BaseLogger object
    found in stutter.logging.
'''

import sys
import unittest

# stutter imports
from stutter.logging import LEVEL
from stutter.logging import BaseLogger


class TestBaseLogger(unittest.TestCase):
    
    def dummy(self, msg=''):
        """ Dummy method used in place of `stdout.write`. """
        self.called = True
    
    def setUp(self):
        self.called = False
        self.logger = BaseLogger(self.dummy, save_logs=False)
    
    def test_log_level(self):
        """ Default logging level should be "message". Can have these values::
            * debug, message, warning, error.
        """
        self.assertEqual(self.logger.get_level(), LEVEL.MESSAGE,
            'BaseLogger uses unexpected default log level')
        
        self.logger.set_level(LEVEL.DEBUG)
        
        self.assertEqual(self.logger.get_level(), LEVEL.DEBUG,
            'BaseLogger failed to set requested log level')
    
    def test_message(self):
        """ Test whether or not the logger calls the expected stuff when
            displaying messages.
        """
        self.logger.message('Testing.')
        self.assertTrue(self.called, 'BaseLogger did not call given output method')
    
    def test_debug(self):
        """ Make sure the logger does not call the output method when it is not
            expected to do so.
        """
        self.logger.debug('Testing')
        self.assertFalse(self.called, 'BaseLogger called given output method at the wrong time')


# EOF
