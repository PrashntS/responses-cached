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

  def test_magic(self):
    obj = RevisionCollection(db='test')

    self.assertEqual(len(obj), 0)

    obj['key'] = 'value'
    self.assertEqual(obj['key'], 'value')
    self.assertEqual(len(obj), 1)

    del obj['key']

    with self.assertRaises(KeyError):
      obj['key']
    self.assertEqual(len(obj), 0)

  @unittest.expectedFailure
  def test_iter(self):
    obj = RevisionCollection(db='test')

    obj['0'] = 0
    obj['1'] = 1
    obj['2'] = 2
    obj['3'] = 3

    for i, v in enumerate(obj):
      self.assertEqual(i, v)

  def test_len(self):
    obj = RevisionCollection(db='test')
    self.assertEqual(len(obj), 0)

  def test_binary(self):
    obj = RevisionCollection(db='test')
    c_ob = set({1, 2, 3, 4, 100})
    obj['outrage'] = c_ob

    self.assertEqual(c_ob, obj['outrage'])

  def test_contains(self):
    obj = RevisionCollection(db='test')

    obj['a'] = 'AA'

    self.assertEqual('a' in obj, True)
    self.assertEqual('b' in obj, False)
