from django.http import HttpResponse
from django.shortcuts import redirect, render
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
from django.contrib.auth.decorators import login_required
import wikipedia
from .forms import UserRegistrationForm


def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method =='POST':
       form = NoteForm(request.POST)
       if form.is_valid():
        notes = Note(user=request.user, title=request.POST['title'],
                        description=request.POST['description']) 
        notes.save()
        messages.success(request,f"Note added from {request.user.username} sucessfully")
    else:
      form = NoteForm()
    notes = Note.objects.filter(user=request.user)
    print(type(request.user))
    context = {"notes": notes ,"form":form }
    return render(request, 'dashboard/notes.html', context)

@login_required
def delete_note(request,pk=None):
    Note.objects.get(id=pk).delete()
    return redirect('notes')

class NoteDetailView(generic.DetailView):
    model= Note
 
@login_required   
def homework(request):
    if request.method =='POST':
       home_form = HomeForm(request.POST)
       if home_form.is_valid():
           try:
            finish = request.POST['Is_finished']
            if finish == 'on':
                finish =True
            else:
                finish = False
           except:
               finish = False
               
       works = Homework(user= request.user, title=request.POST['title'],
                     subject= request.POST['subject'],
                        description= request.POST['description'],
                        due= request.POST['due'],
                        Is_finished= finish) 
       works.save()
       messages.success(request,f"Homework added from {request.user.username} sucessfully")
    
    form = HomeForm()
    work = Homework.objects.filter(user=request.user)
    if len(work)== 0:
        work_done=True
        
    else:
     work_done= False 
      
    context = {"works": work ,"works_done": work_done , 'form':form }
    # print(context)
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request,pk= None):
    work = Homework.objects.get(id = pk)
    if work.Is_finished ==True:
       work.Is_finished = False
    else:
     work.Is_finished =True
     work.save()
    return redirect('home-work')

@login_required    
def delete_work(request,pk=None):
    Homework.objects.get(id = pk).delete()
    return redirect('home-work')  

def youtube(request):
    if request.method == 'POST':
        form=DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=20)
        result_list =[]
        for i in video.result()['result']:
            result_dict = {
            'input':text,
            'title':i['title'],
            'thumbnails':i['thumbnails'][0]['url'],
            'channel':i['channel']['name'],
            'link':i['link'],
            'duration':i['duration'],
            'views':i['viewCount']['short'],
            'published':i['publishedTime'],


            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
                    result_dict['description']= desc
                    result_list.append (result_dict)
                    context={
                        'form':form, 'results':result_list
                    }
                    return render(request,'dashboard/youtube.html',context)
    else:   
     form = DashboardForm()
    context={'form':form}
    return render(request,'dashboard/youtube.html',context)  

@login_required
def todo(request):
    if request.method =='POST':
       form= TodoForm(request.POST)
       if form.is_valid():
           try:
            finished = request.POST['Is_finished']
            if finished == 'on':
                finished =True
            else:
                finished = False
           except:
               finished = False
             
       todo = Todo(user=request.user, title=request.POST['title'],
                    Is_finished =finished

                        ) 
       todo.save()
       messages.success(request,f"Todo added from {request.user.username} sucessfully")
    else:
     form = TodoForm()
    todo= Todo.objects.filter(user=request.user)
    
    if len(todo) == 0:
        todo_done= True
    else:
        todo_done= False
    context={'todos':todo , 'form':form, 'todos_done':todo_done}
    return render(request,'dashboard/todo.html',context)

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id = pk).delete()
    messages.success(request,f"Todo deleted from {request.user.username} !!")
    return redirect('todo')

@login_required
def update_todo(request,pk= None):
    todo = Todo.objects.get(id = pk)
    if todo.Is_finished ==True:
       todo.Is_finished = False
    else:
     todo.Is_finished =True
     todo.save()
    return redirect('todo')
    
def Books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
        context = {'form': form, 'results': result_list}
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/books.html', context)

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        r = requests.get(url)
        answer = r.json()
        
        try:
            phonetics= answer[0]['phonetics'][0]['text']
            audio= answer[0]['phonetics'][0]['audio']
            # print('audio',audio)
            definition= answer[0]['meanings'][0]['definitions'][0]
            examples= answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms= answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'examples':examples,
                'synonyms':synonyms
                
            }
        except:
            context={
                'form':form,
                'input':'',
                }
        return render(request,'dashboard/dictionary.html',context)
    else:
       form = DashboardForm()
       context = {'form':form}
    return render(request,'dashboard/dictionary.html',context)

def wiki(request):
    if request.method =="POST":
        text=request.POST['text']
        
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form' :form,
            'title':search.title,
            'link': search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    else:
     form=DashboardForm()
     context= {'form':form}
    return render(request,'dashboard/wiki.html',context)

@login_required
def Conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        measurement_type = request.POST.get('measurement')

        if measurement_type == 'length':
            measurement_form = ConversionLengthForm()
        elif measurement_type == 'mass':
            measurement_form = ConversionMassForm()
        else:
            measurement_form = None

        context = {
            'form': form,
            'm_form': measurement_form,
            'input': True,
        }

        if 'input' in request.POST:
            first = request.POST.get('measure1')
            second = request.POST.get('measure2')
            input_value = request.POST.get('input')
            answer = ''

            if input_value and input_value.isdigit() and int(input_value) >= 0:
                input_value = int(input_value)
                if measurement_type == 'length':
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {input_value * 3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {input_value / 3} yard'
                elif measurement_type == 'mass':
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {input_value * 0.453592} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {input_value * 2.20462} pound'

                context['answer'] = answer

        return render(request, 'dashboard/conversion.html', context)

    else:
        form = ConversionForm()
        context = {'form': form, 'input': False}
        return render(request, 'dashboard/conversion.html', context)


# def Conversion(request):
#     if request.method == 'POST':
#         form = ConversionForm(request.POST)
#         if request.POST['measurement'] == 'length':
#             measurement_form = ConversionLengthForm()
#             context={'form':form, 
#                      'm_form':measurement_form,
#                      'input':True
#                      }
#             # to check if input is true
#             if 'input' in request.POST:
#                 first = request.POST['measure1']
#                 second = request.POST['measure2']
#                 input = request.POST['input']
#                 answer =''
#                 if input and int(input) >= 0:
#                     if first == 'yard' and second == 'foot':
#                         answer = f'{input} yard = {int(input)*3} foot'
#                     if first == 'foot' and second == 'yard':
#                         answer = f'{input} foot = {int(input)/3} yard'
#                         context= {'form':form, 
#                               'm_form':measurement_form,
#                               'input':True,
#                               'answer':answer
#                               } 
    #     if request.POST['measurement'] == 'mass':
    #         measurement_form = ConversionMassForm()
    #         context={'form':form, 'm_form':measurement_form,'input':True}
    #         # to check if input is true
    #         if 'input'in request.POST:
    #             first = request.POST['measure1']
    #             second = request.POST['measure2']
    #             input = request.POST['input']
    #             answer =''
    #             if input and int(input)>= 0:
    #                 if first == 'pound' and second == 'kilogram':
    #                     answer = f'{input} pound = {int(input)*0.453592} kilogram'
    #                 if first == 'kilogram' and second == 'pound':
    #                     answer = f'{input}kilogram = {int(input)*2.20462} pound'
    #                 context= {'form':form,  
    #                           'm_form':measurement_form,
    #                           'input':True,
    #                           'answer':answer
    #                           }  
    #         return render(request, 'dashboard/conversion.html', context)

    # else:  
    #  form = ConversionForm()
    #  context ={'form':form, 'input':False}
    #  return render (request,'dashboard/conversion.html',context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username} Successfully!!")
        return redirect('login') 
        
    else:   
     form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    work = Homework.objects.filter(Is_finished=False, user=request.user)
    todo = Todo.objects.filter(Is_finished=False, user=request.user)
    
    if len(work) == 0:
        work_done = True
    else:
        work_done = False    
    if len(todo) == 0:
        todo_done = True
    else:
      todo_done = False
    context = {'works': work, 'todos':todo, 'work_done':work_done, 'todo_done':todo_done}
    return render(request,'dashboard/profile.html',context) 



# def logout(request):
#     if request.method == 'POST':
#         logout(request)
#         messages.success(request,f" Logout {request.user.username} sucessfully")
#     return render(request, 'dashboard/logout.html')
     
        