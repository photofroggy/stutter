''' Reflex setup.
'''

from distutils.core import setup

setup(name='stutter',
    version='1.1',
    description='Logging objects for Python apps.',
    author='photofroggy',
    author_email='froggywillneverdie@msn.com',
    url='http://photofroggy.github.com/stutter/index.html',
    packages=[
        'stutter',
        'stutter.test'
    ],
    platforms=['Any'],
    classifiers=[
        'Natural Language :: English',
        'Development Status :: 4 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Topic :: Utilities'
    ],
    long_description="""
**Stutter** is my own idea for a simple logging lib. Objects in the package handle
timestamps and logging to files automatically. Logging to files can be buffered,
and even threaded, according to your application's needs.

Note that it may be possible to use the BufferedReader object with twisted to
eliminate the need for threading. I may create such an object in future.

-------------
Brief example
-------------

Use objects from this package if you want to log messages. I intend to use this
in a bot, and possibly a client, for the deviantART chat network. Logging can
be done as follows::
    
    from stutter import logging
    
    logger = logging.BaseLogger()
    logger.message('Sup homie?')
    logger.message('Everything is saved to files in `./log` by default')
    logger.message('You can change this somehow... I\'ll explain later.')
    logger.debug('This message won't be printed on-screen, but will be saved.')

    
----------------
Buffered logging
----------------

File IO can be expensive sometimes, so you can use the BufferedLogger object
to determine when messages should be saved to files. When a BufferedLogger is
used to display log messages on screen, the messages are displayed instantly,
but they not saved to any files until `.push()` is used::
    
    import time
    from stutter import logging
    
    logger = logging.BufferedLogger()
    logger.message('Some boring message...')
    time.sleep(5)
    # You can use the time you have to confirm that no logs have been written
    # yet, if you like. These are really trivial examples...
    logger.warning('Writing logs!')
    logger.push()

Note that `.push()` will only save up to 5 messages at a time. You can change
this by telling `push` how many messages to save using the `limit` parameter.
For example, to save up to 10 messages, you would call `.push(limit=10)`. To
push **all** stored messages to log files, call `.push(limit=0)`.

----------------
Threaded logging
----------------

If you want to automate calls to `push` without having to really think about it
too much, you can use the `ThreadedLogger` object. A brief and naive example::
    
    from stutter import logging
    
    logger = logging.ThreadedLogger()
    # Start pushing in a thread.
    logger.start()
    logger.message('Your mother smells of elderberries.')
    # Stop the threading stuff.
    logger.stop()
    # Wait until the thread has actually stopped.
    logger.join()
    # Make sure all log messages have been saved.
    # This is not done by stopping the thread!
    logger.push(0)

=============
Documentation
=============

I will write documentation when I can be arsed.
"""
)

# EOF
