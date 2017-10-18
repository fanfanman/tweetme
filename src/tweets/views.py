# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin

# Create your views here.
# create, retrieve, update, delete

# create
class TweetCreateView(FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/create_view.html"
	# success_url = "/tweet/create/"


# retrieve
class TweetDetailView(DetailView):
	#template_name = "tweets/detail_view.html"
	queryset = Tweet.objects.all()

	#def get_object(self):
	#	pk = self.kwargs.get("pk")
	#	return Tweet.objects.get(id=pk)


class TweetListView(ListView):
	#template_name = "tweets/list_view.html"
	queryset = Tweet.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		#print(context)
		return context


'''def tweet_detail_view(request, id=1):
	obj = Tweet.objects.get(id=id)
	print(obj)
	context = {
		"object": obj
	}
	return render(request, "tweets/detail_view.html", context)'''

'''def tweet_list_view(request):
	queryset = Tweet.objects.all()
	print(queryset)
	context = {
		"object_list": queryset
	}
	return render(request, "tweets/list_view.html", context)'''