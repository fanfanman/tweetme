# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

# Create your tests here.

from .models import Tweet

User = get_user_model()

class TweetModelTestCase(TestCase):
	def setUp(self):
		some_random_user = User.objects.create(username='aprilzzzzz')

	def test_tweet_item(self):
		obj = Tweet.objects.create(
				user= User.objects.first(),
				content='Some random content here'
			)
		self.assertTrue(obj.content == 'Some random content here')
		self.assertTrue(obj.id == 1)
		
	def test_tweet_url(self):
		obj = Tweet.objects.create(
				user= User.objects.first(),
				content='Some random content here'
			)
		absolute_url = reverse("tweet:detail", kwargs={"pk": obj.pk})
		self.assertEqual(obj.get_absolute_url(), absolute_url)