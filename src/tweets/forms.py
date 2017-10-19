from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = [
			#"user",
			"content"
		]
		#exclude = []

	#example of validation error in forms.py
	def clean_content(self, *args, **kwargs):
		#built in validation for field
		content = self.cleaned_data.get("content")
		if content == "abc":
			raise forms.ValidationError("cannot be abs")
		return content