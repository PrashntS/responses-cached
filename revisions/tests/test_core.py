#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Revisions
import unittest
import requests
import mongomock

from revisions.core import RequestsMock, RevisionCollection

try:
  from unittest import mock
except ImportError:
  import mock


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


@mock.patch('pymongo.MongoClient', mongomock.MongoClient)
class TestRivisionCollection(unittest.TestCase):
  def test_object(self):
    obj = RevisionCollection(db='test')
