#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Revisions
import unittest
import requests

from revisions.core import RequestsMock

class TestRequestsMock(unittest.TestCase):
  def test_object(self):
    obj = RequestsMock()

  def test_context(self):
    obj = RequestsMock()

    url = 'http://doom.0xc0d3.pw'

    def callback(method, url_, *a):
      self.assertEqual(method, 'get')
      self.assertEqual(url_, url)

    obj.callback = callback

    with obj as context:
      requests.get(url)
