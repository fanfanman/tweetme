from django import forms
from django.forms.utils import ErrorList

class FormUserNeededMixin(object):

     def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
            return super(FormUserNeededMixin, self).form_valid(form)
        else:
            form.add_error("content", "This user is not allowed to change this data.")
            return self.form_invalid(form)

class UserOwnerMixin(object):
	def form_valid(self, form):
		if form.instance.user == self.request.user:
			return super(UserOwnerMixin, self).form_valid(form)
		else:
			form.add_error("content", "This user is not alllowed to change")
			return self.form_invalid(form)
