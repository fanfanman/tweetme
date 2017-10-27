# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
from hashtags.signals import parsed_hashtags
from .validators import validate_content

class TweetManager(models.Manager):
	def retweet(self, user, parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj

		qs = self.get_queryset().filter(
			user=user, parent=og_parent
			).filter(
				timestamp__year = timezone.now().year,
				timestamp__month = timezone.now().month,
				timestamp__day = timezone.now().day
				)
		if qs.exists():
			return None

		obj = self.model(
				parent = og_parent,
				user = user,
				content = parent_obj.content,
			)
		obj.save()

		return obj

	def like_toggle(self, user, tweet_obj):
		if user in tweet_obj.liked.all():
			is_liked = False
			tweet_obj.liked.remove(user)
		else:
			is_liked = True
			tweet_obj.liked.add(user)
		return is_liked


class Tweet(models.Model):
	parent 		= models.ForeignKey("self", blank=True, null=True)
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, default =1)
	content 	= models.CharField(max_length=140, validators=[validate_content])
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)
	liked 		= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')

	objects = TweetManager()
	def __str__(self):
		return str(self.content)

	def get_absolute_url(self):
		return reverse("tweet:detail", kwargs={"pk":self.pk})

	class Meta:
		ordering = ['-timestamp']

	''' example of inbuilt model raiseerror function
	def clean(self, *args, **kwargs):
		# inside inbuilt model function
		content = self.content
		if content == "abc":
			raise ValidationError("Cannot be abc")
		return super(Tweet, self).clean(*args, **kwargs)'''

def tweet_save_receiver(sender, instance, created, *args, **kwargs):
	if created and not instance.parent:
		# notify a user
		user_regex = r'@(?P<username>[\w.@+-]+)'
		usernames = re.findall(user_regex, instance.content)
		# send notification to user here

		hash_regex = r'#(?P<hashtag>[\w\d-]+)'
		hashtags = re.findall(hash_regex, instance.content)
		parsed_hashtags.send(sender=instance.__class__, hashtag_list = hashtags)
		# send hashtag singal to user here

post_save.connect(tweet_save_receiver, sender=Tweet)
