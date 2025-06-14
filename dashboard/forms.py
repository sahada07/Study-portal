from . models import *
from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title','description']
        
class DateInput(forms.DateInput):
    input_type ="date"
    
class HomeForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject', 'title', 'description','due','Is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length= 100,label="Enter Your Search:")
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','Is_finished']

class ConversionForm(forms.Form):
    CHOICES= [('length','Length'),('mass','Mass')]
    measurement= forms.ChoiceField(choices= CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES= [('yard','Yard'),('foot','Foot')]  
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number', 'placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(
        label='', widget = forms.Select(choices=CHOICES)
        
        )
    measure2 = forms.CharField(
        label='', widget = forms.Select(choices=CHOICES)
     )
          
class ConversionMassForm(forms.Form):
    CHOICES= [('pound','Pound'),('kilogram','Kilogram')]  
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number', 'placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(
        label='', widget = forms.Select(choices=CHOICES)
        
        )
    measure2 = forms.CharField(
        label='', widget = forms.Select(choices=CHOICES)
     )            

      
class UserRegistrationForm(UserCreationForm):
    email= forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

