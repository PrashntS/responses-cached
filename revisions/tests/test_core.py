#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Revisions
import unittest
import requests
import mongomock
from time import sleep

from datetime import timedelta, datetime

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

  def test_access(self):
    obj = RevisionCollection(db='test', resolution=timedelta(milliseconds=1))

    ins1 = 100
    ins2 = 200

    obj['test'] = ins1
    _acc_time_1 = datetime.now()
    self.assertEqual(obj['test'], ins1)

    # Wait for a second -- resolution!
    sleep(1)

    # Update Revision -- W
    obj['test'] = ins2
    _acc_time_2 = datetime.now()
    self.assertEqual(obj['test'], ins2)

    # Obtain oldest revision
    self.assertEqual(obj['test', 0], ins1)

    # Obtain latest revision
    self.assertEqual(obj['test', -1], ins2)

    # Obtain timed revisions
    self.assertEqual(obj['test', _acc_time_1], ins1)
    self.assertEqual(obj['test', _acc_time_2], ins2)

    # Fail on bad revision time
    with self.assertRaises(KeyError):
      obj['test', datetime.now() - timedelta(days=1)]

