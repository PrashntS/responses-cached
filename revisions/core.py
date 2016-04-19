#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Revisions
import requests

try:
  from unittest import mock
except ImportError:
  import mock


class Revisions(object):
  def __init__(self):
    self._req_get = requests.get

  def __enter__(self):
    self.start()
    return self

  def __exit__(self, *args):
    self.stop()

  def _get_patch(self, *a, **kwa):
    return self._req_get(*a, **kwa)

  def start(self):
    def on_get(*a, **kwa):
      return self._get_patch(*a, **kwa)

    self._patcher = mock.patch('requests.get', on_get)
    self._patcher.start()

  def stop(self):
    self._patcher.stop()
