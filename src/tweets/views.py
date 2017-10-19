# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin

# Create your views here.
# create, retrieve, update, delete

# create
class TweetCreateView(FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/create_view.html"
	login_url = '/admin/'


# update
class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	# success_url = "/tweet/"


# retrieve
class TweetDetailView(DetailView):
	#template_name = "tweets/detail_view.html"
	queryset = Tweet.objects.all()

	#def get_object(self):
	#	pk = self.kwargs.get("pk")
	#	return Tweet.objects.get(id=pk)


class TweetListView(ListView):
	# template_name = "tweets/list_view.html"
	# queryset = Tweet.objects.all()

	def get_queryset(self, *args, **kwargs):
		qs = Tweet.objects.all()
		print(self.request.GET)
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		#print(context)
		return context

# delete
class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	success_url = reverse_lazy("tweet:list")
	template_name = "tweets/delete_confirm.html"


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