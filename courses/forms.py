from django import forms
from .models import Course,SectionVideo
from taggit.models import Tag 

class CourseCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(label='Tags', queryset=Tag.objects.order_by('name'),widget=forms.SelectMultiple)
   #  active = forms.BooleanField(widget=forms.CheckboxInput (attrs={'class':'form-check-input','type':'checkbox'}))
    price : forms.CharField()
    class Meta:
        model = Course
        fields = ["name","description","price","discount","thumbnail","resource","length","tags","prerequisite","learning","active"]
        widgets = {
             'description' : forms.Textarea(attrs={'class':'form-control'}),

         } 
    def __init__(self, *args, **kwargs):
          super(CourseCreateForm, self).__init__(*args, **kwargs)
          self.fields['name'].widget.attrs['class'] = 'form-control'
          self.fields['description'].widget.attrs['class'] = 'form-control'
          self.fields['price'].widget.attrs['class'] = 'form-control'
          self.fields['length'].widget.attrs['class'] = 'form-control'
          self.fields['discount'].widget.attrs['class'] = 'form-control'
          self.fields['thumbnail'].widget.attrs['class'] = 'form-control'
          self.fields['resource'].widget.attrs['class'] = 'form-control'
          self.fields['prerequisite'].widget.attrs['class'] = 'form-control'
          self.fields['learning'].widget.attrs['class'] = 'form-control'
          self.fields['active'].widget.attrs['class'] = 'form-check-input'
         #  for field in self.fields:
         #       self.fields[field].widget.attrs['class'] = 'form-control'
          
class CourseActivation(forms.ModelForm):
   
   class Meta:
      model = Course
      fields = "__all__"
      widgets = {
         "active":forms.CheckboxInput(attrs={'class':'form-check-input','type':'checkbox'})
      }
      
class SectionForm(forms.ModelForm):
   
   class Meta:
      model = SectionVideo
      fields = ["name","serial_number"]
      widgets = {
             'name' : forms.TextInput(attrs={'class':'form-control'}),
         } 
   def __init__(self, *args, **kwargs):
          super(SectionForm, self).__init__(*args, **kwargs)
          self.fields['serial_number'].widget.attrs['class'] = 'form-control'
   def clean(self):
          cleaned_data = super(SectionForm, self).clean()
         #  password = cleaned_data.get('password')
         #  confirm_password = cleaned_data.get('confirm_password')
