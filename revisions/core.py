#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Revisions
import requests.adapters.HTTPAdapter.send

from unittest import mock


class Revisions(object):
  def __init__(self):
    self._req_send_orig = requests.adapters.HTTPAdapter.send

  def __enter__(self):
    self.start()
    return self

  def __exit__(self, *args):
    self.stop()

  def _on_send_patch(self, adapter, request, *a, **kwa):
    return self._req_send_orig(adapter, request, *a, **kwa)

  def start(self):
    def on_send(*a, **kwa):
      return self._on_send_patch(*a, **kwa)

    self._patcher = mock.patch('requests.adapters.HTTPAdapter.send', on_send)
    self._patcher.start()

  def stop(self):
    self._patcher.stop()
