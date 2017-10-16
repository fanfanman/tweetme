# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

# Create your models here.

class Tweet(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	content 	= models.CharField(max_length=140)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.content)