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

    with obj as context:
      requests.get('http://google.com')
