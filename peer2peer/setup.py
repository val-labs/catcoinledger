#!/usr/bin/env python
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(name='peer2peer',
      version='1.8.1',
      description='peer 2 peer',
      py_modules=['peer2peer'],
      scripts=['peer2peer.py'],
      license='MIT',
      platforms='any',
      install_requires=[
          'websocket-client',
          'gevent-websocket',
          'gevent','future'
          ],
)
