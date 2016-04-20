#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Revisions
import requests
import hashlib
import pymongo

try:
  from unittest import mock
except ImportError:
  import mock


class Revision(object):
  '''
  '''

  def __init__(self, oid, collection, version=None):
    self.version = version

  @property
  def versions(self):
    '''Obtain available versions of the document.

    Returns a chronologically sorted list of versions of this document.
    '''
    pass


class RevisionCollection(object):
  '''Dictionary interface for Revisions in MongoDB.
  '''

  def __init__(self, db, host='localhost', port=27017, **kwa):
    ''''''
    self._connection = pymongo.MongoClient(host, port, **kwa)
    self._db = self._connection[db]
    self._collection = self._db['revisions']

  def __len__(self):
    return self._collection.count()

  def __getitem__(self, key):
    doc = self._collection.find_one({'k': key})
    if doc is None:
      raise KeyError('Invalid Key')
    return doc['v']

  def __setitem__(self, key, value):
    self._collection.update_one(
        {'k': key},
        {'$set': {'v': value}},
        upsert=True)

  def __delitem__(self, key):
    self._collection.delete_one({'k': key})

  def __iter__(self):
    for obj in self._collection.find():
      yield obj['v']

  def __contains__(self, key):
    return self._collection.find_one({'k': key}) is not None


class RequestsMock(object):
  '''
  '''

  def __init__(self):
    '''
    '''
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
