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
    self.__request_org = requests.request

  def __enter__(self):
    self.start()
    return self

  def __exit__(self, *args):
    self.stop()

  def __request_patch(self, method, url, *a, **kwa):
    response = self.__request_org(method, url, *a, **kwa)
    self.callback(method, url, response)
    return response

  @property
  def callback(self):
    try:
      return self.__callback
    except AttributeError:
      return lambda *x: None

  @callback.setter
  def callback(self, func):
    self.__callback = func

  def start(self):
    def delegate(*a, **kwa):
      return self.__request_patch(*a, **kwa)

    self._patcher = mock.patch('requests.api.request', delegate)
    self._patcher.start()

  def stop(self):
    self._patcher.stop()
