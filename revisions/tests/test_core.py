#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Revisions
import unittest
import requests

from revisions.core import Revisions

class TestRevisions(unittest.TestCase):
  def test_object(self):
    obj = Revisions()

  def test_context(self):
    obj = Revisions()

    url = 'http://0xc0d3.pw'

    def callback(method, url_, *a):
      self.assertEqual(method, 'get')
      self.assertEqual(url_, url)

    obj.callback = callback

    with obj as context:
      requests.get(url)
