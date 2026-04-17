from django import forms
from .models import AddBlog

class blog_form(forms.ModelForm):
    class Meta:
        model = AddBlog
        fields = '__all__'
        # fields = ('Name', 'Title','Summery', 'Image')

        widget = {
            'Name' : forms.TextInput(attrs={'class':'form-control  '}),
            'Image': forms.ImageField(),

            'Title': forms.TextInput(attrs={'class': 'form-control  '}),
            'Summery': forms.Textarea(attrs={'class': 'form-control  '}),
        }

