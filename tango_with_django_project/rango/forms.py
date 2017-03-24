from django import forms
from rango.models import Page, Category
from django.utils.translation import ugettext_lazy as _

class CategoryForm(forms.ModelForm):
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)
        help_texts = {
            'name': _("Please enter the category name."),
        }

class PageForm(forms.ModelForm):

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # if url is not empty and doesn't start with 'http://',
        # then prepend 'http://'
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present
        # Some fields may allow NULL values, so we may not want to include them
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        help_texts = {
            'title': _("Please enter the title of the page."),
            'url': _("Please enter the URL of the page.")
        }
        # or specify the fields to include (i.e. not include the category field)
        # fields = ('title', 'url', 'views')
