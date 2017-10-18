# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models

# Create your models here.
from .validators import validate_content

class Tweet(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	content 	= models.CharField(max_length=140, validators=[validate_content])
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.content)

	''' example of inbuilt model raiseerror function
	def clean(self, *args, **kwargs):
		# inside inbuilt model function
		content = self.content
		if content == "abc":
			raise ValidationError("Cannot be abc")
		return super(Tweet, self).clean(*args, **kwargs)'''