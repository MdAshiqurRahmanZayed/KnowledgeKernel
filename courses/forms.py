from django import forms
from .models import Course,SectionVideo,Video,Assessment,SubmittedAssessment,Mark
from taggit.models import Tag 

class CourseCreateForm(forms.ModelForm):
   #  tags = forms.ModelMultipleChoiceField(label='Tags', queryset=Tag.objects.order_by('name'),widget=forms.SelectMultiple)
    tags = forms.ModelMultipleChoiceField(label='Tags', queryset=Tag.objects.order_by('name'),widget=forms.SelectMultiple)
   #  tags = forms.CharField(queryset=Tag.objects.order_by('name'),widget=forms.SelectMultiple)
   #  active = forms.BooleanField(widget=forms.CheckboxInput (attrs={'class':'form-check-input','type':'checkbox'}))
    class Meta:
        model = Course
        fields = ["name","description","price","discount","thumbnail","tags","resource","length","prerequisite","learning","active"]
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
         
class VideoForm(forms.ModelForm):
   class Meta:
      model = Video
      fields = ["title","video_description","serial_number","video_id","resource","resource_title","is_preview"]
      
      widgets= {
         "video_description" : forms.Textarea()
      }
   def __init__(self, *args, **kwargs):
          super(VideoForm, self).__init__(*args, **kwargs)
          self.fields['title'].widget.attrs['class'] = 'form-control'
          self.fields['video_description'].widget.attrs['class'] = 'form-control'
          self.fields['serial_number'].widget.attrs['class'] = 'form-control'
          self.fields['resource'].widget.attrs['class'] = 'form-control'
          self.fields['resource_title'].widget.attrs['class'] = 'form-control'
          self.fields['video_id'].widget.attrs['class'] = 'form-control'
          self.fields['is_preview'].widget.attrs['class'] = 'form-check-input'

class AssessmentForm(forms.ModelForm):
   class Meta:
      model = Assessment
      fields = ['title','resource','resource_title','maximum_number']
   def __init__(self, *args, **kwargs):
         super(AssessmentForm, self).__init__(*args, **kwargs)
         self.fields['title'].widget.attrs['class'] = 'form-control'
       
         self.fields['resource'].widget.attrs['class'] = 'form-control'
         self.fields['resource_title'].widget.attrs['class'] = 'form-control'
         self.fields['maximum_number'].widget.attrs['class'] = 'form-control'
         
         
class SubmittedAssessmentForm(forms.ModelForm):
   class Meta:
      model = SubmittedAssessment
      fields = ['resource_title','resource']
   def __init__(self, *args, **kwargs):
         super(SubmittedAssessmentForm, self).__init__(*args, **kwargs)       
         self.fields['resource'].widget.attrs['class'] = 'form-control'
         self.fields['resource'].widget.attrs['placeholder'] = 'Resource link'
         self.fields['resource_title'].widget.attrs['class'] = 'form-control'
         
         
class MarkForm(forms.ModelForm):
   class Meta:
      model = SubmittedAssessment
      fields = ['obtained_mark','feedback']
      # fields = ['obtained_mark','feedback']
   def __init__(self, *args, **kwargs):
         super(MarkForm, self).__init__(*args, **kwargs)       
         self.fields['obtained_mark'].widget.attrs['class'] = 'form-control'
         self.fields['feedback'].widget.attrs['class'] = 'form-control'
   