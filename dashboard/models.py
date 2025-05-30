from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user= models.ForeignKey(User,on_delete = models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    
    def __str__(self):
       return self.title

# to get rid of extra s in db
# class Meta:
#     verbose_name ="notes" 
#     verbose_name_plural="notes"

class Homework(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    subject= models.CharField(max_length=50)
    title=models.CharField(max_length=100)
    description=models.TextField()
    due=models.DateTimeField()
    Is_finished=models.BooleanField(default=False)
    
    def __str__(self):
        return self.subject
  
class Todo(models.Model): 
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 title=models.CharField(max_length=225)  
 Is_finished=models.BooleanField(default=False)

def __str__(self):
        return self.title