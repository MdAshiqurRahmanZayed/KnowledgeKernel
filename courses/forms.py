from django import forms
from .models import Course
from taggit.models import Tag 

class CourseCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(label='Tags', queryset=Tag.objects.order_by('name'),widget=forms.SelectMultiple)
    
    
    class Meta:
        model = Course
        fields = ["name","description","price","discount","thumbnail","resource","length","tags","prerequisite","learning","active"]
        widgets = {
             'name' : forms.TextInput(attrs={'class':'form-control  '}),
             'description' : forms.Textarea(attrs={'class':'form-control'}),
          #    'price' : forms.TextInput(attrs={'class':'form-control'}),
          #    'discount' : forms.TextInput(attrs={'class':'form-control'}),
             
          #    'length' : forms.TextInput(attrs={'class':'form-control'}),
             'prerequisite' : forms.TextInput(attrs={'class':'form-control'}),
             'learning' : forms.TextInput(attrs={'class':'form-control'}),
            #  'tags' : forms.Textarea(attrs={'class':'form-control'}),
             
         } 