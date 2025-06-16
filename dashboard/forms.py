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

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for better styling
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user      
# class UserRegistrationForm(UserCreationForm):
#     email= forms.EmailField(required=True)
    
#     class Meta:
#         model = User
#         fields = ['username','email','password1','password2']

