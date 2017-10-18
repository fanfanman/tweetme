from django import forms
from django.forms.utils import ErrorList

class FormUserNeededMixin(object):

     def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
            return super(FormUserNeededMixin, self).form_valid(form)
        else:
            form.add_error("content", "User must be logged in")
            return self.form_invalid(form)