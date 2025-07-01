import os
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
from django.contrib.auth.views import LoginView
from django.contrib import messages


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
    messages.success(request,f"Note deleted from {request.user.username} !!")
    return redirect('notes')

class NoteDetailView(generic.DetailView):
    model= Note
 
@login_required   
# def homework(request):
#     if request.method =='POST':
#        home_form = HomeForm(request.POST)
#        if home_form.is_valid():
#            try:
#             finish = request.POST['Is_finished']
#             if finish == 'on':
#                 finish =True
#             else:
#                 finish = False
#            except:
#                finish = False
               
#        works = Homework(user= request.user, title=request.POST['title'],
#                      subject= request.POST['subject'],
#                         description= request.POST['description'],
#                         due= request.POST['due'],
#                         Is_finished= finish) 
#        works.save()
#        messages.success(request,f"Homework added from {request.user.username} sucessfully")
    
#     form = HomeForm()
#     work = Homework.objects.filter(user=request.user)
#     if len(work)== 0:
#         work_done=True
        
#     else:
#      work_done= False 
      
#     context = {"works": work ,"works_done": work_done , 'form':form }
#     # print(context)
#     return render(request, 'dashboard/homework.html', context)
def homework(request):
    if request.method == 'POST':
        # Check if this is an update request for existing homework
        if 'homework_id' in request.POST:
            # Handle updating existing homework completion status
            homework_id = request.POST['homework_id']
            try:
                homework_item = Homework.objects.get(id=homework_id, user=request.user)
                # Check if checkbox was checked (will be 'on') or unchecked (won't exist in POST)
                homework_item.Is_finished = 'Is_finished' in request.POST
                homework_item.save()
                
                status = "completed" if homework_item.Is_finished else "marked as incomplete"
                messages.success(request, f"Homework '{homework_item.title}' {status}")
            except Homework.DoesNotExist:
                messages.error(request, "Homework not found")
        
        else:
            # Handle creating new homework
            home_form = HomeForm(request.POST)
            if home_form.is_valid():
                try:
                    finish = request.POST.get('Is_finished', False)
                    if finish == 'on':
                        finish = True
                    else:
                        finish = False
                except:
                    finish = False
                
                works = Homework(
                    user=request.user, 
                    title=request.POST['title'],
                    subject=request.POST['subject'],
                    description=request.POST['description'],
                    due=request.POST['due'],
                    Is_finished=finish
                )
                works.save()
                messages.success(request, f"Homework added from {request.user.username} successfully")
    
    # Always render the page with current data
    form = HomeForm()
    work = Homework.objects.filter(user=request.user)
    work_done = len(work) == 0
    
    context = {"works": work, "works_done": work_done, 'form': form}
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request, pk=None):
    work = Homework.objects.get(id=pk)
    work.Is_finished = not work.Is_finished  # Toggle the boolean value
    work.save()
    return redirect('home-work')

@login_required    
def delete_work(request,pk=None):
    Homework.objects.get(id = pk).delete()
    messages.success(request,f"Homework deleted from {request.user.username} !!")
    return redirect('home-work')  

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=20)
        result_list = []
        
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'thumbnail': i['thumbnails'][0]['url'],  # Fixed: was 'thumbnails'
                'channel': i['channel']['name'],
                'link': i['link'],
                'duration': i['duration'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            
            # Handle description
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            
            # Add to result list
            result_list.append(result_dict)
        
        # Return context with all results
        context = {
            'form': form, 
            'results': result_list
        }
        return render(request, 'dashboard/youtube.html', context)
    
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/youtube.html', context)
    
    # if request.method == 'POST':
    #     form=DashboardForm(request.POST)
    #     text = request.POST['text']
    #     video = VideosSearch(text, limit=20)
    #     result_list =[]
    #     for i in video.result()['result']:
    #         result_dict = {
    #         'input':text,
    #         'title':i['title'],
    #         'thumbnails':i['thumbnails'][0]['url'],
    #         'channel':i['channel']['name'],
    #         'link':i['link'],
    #         'duration':i['duration'],
    #         'views':i['viewCount']['short'],
    #         'published':i['publishedTime'],


    #         }
    #         desc = ''
    #         if i['descriptionSnippet']:
    #             for j in i['descriptionSnippet']:
    #                 desc += j['text']
    #                 result_dict['description']= desc
    #                 result_list.append (result_dict)
    #                 context={
    #                     'form':form, 'results':result_list
    #                 }
    #                 return render(request,'dashboard/youtube.html',context)
    # else:   
    #  form = DashboardForm()
    # context={'form':form}
    # return render(request,'dashboard/youtube.html',context)  

@login_required
# def todo(request):
#     if request.method =='POST':
#        form= TodoForm(request.POST)
#        if form.is_valid():
#            try:
#             finished = request.POST['Is_finished']
#             if finished == 'on':
#                 finished =True
#             else:
#                 finished = False
#            except:
#                finished = False
             
#        todo = Todo(user=request.user, title=request.POST['title'],
#                     Is_finished =finished

#                         ) 
#        todo.save()
#        messages.success(request,f"Todo added from {request.user.username} sucessfully")
#     else:
#      form = TodoForm()
#     todo= Todo.objects.filter(user=request.user)
    
#     if len(todo) == 0:
#         todo_done= True
#     else:
#         todo_done= False
#     context={'todos':todo , 'form':form, 'todos_done':todo_done}
#     return render(request,'dashboard/todo.html',context)

def todo(request):  # Replace with your actual function name
    if request.method == 'POST':
        # Check if this is an update request for existing todo
        if 'todo_id' in request.POST:
            # Handle updating existing todo completion status
            todo_id = request.POST['todo_id']
            try:
                todo_item = Todo.objects.get(id=todo_id, user=request.user)
                # Check if checkbox was checked (will be 'on') or unchecked (won't exist in POST)
                todo_item.Is_finished = 'Is_finished' in request.POST
                todo_item.save()
                
                status = "completed" if todo_item.Is_finished else "marked as incomplete"
                messages.success(request, f"Todo '{todo_item.title}' {status}")
            except Todo.DoesNotExist:
                messages.error(request, "Todo not found")
        
        else:
            # Handle creating new todo
            form = TodoForm(request.POST)
            if form.is_valid():
                try:
                    finished = request.POST.get('Is_finished', False)
                    if finished == 'on':
                        finished = True
                    else:
                        finished = False
                except:
                    finished = False
                
                todo = Todo(
                    user=request.user, 
                    title=request.POST['title'],
                    Is_finished=finished
                )
                todo.save()
                messages.success(request, f"Todo added for {request.user.username} successfully")
    
    # Always render the page with current data
    form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    todo_done = len(todo) == 0
    
    context = {'todos': todo, 'form': form, 'todos_done': todo_done}
    return render(request, 'dashboard/todo.html', context)

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id = pk).delete()
    messages.success(request,f"Todo deleted from {request.user.username} !!")
    return redirect('todo')

@login_required
def update_todo(request,pk= None):
    todo = Todo.objects.get(id=pk)
    todo.Is_finished = not todo.Is_finished  # Toggle the boolean value
    todo.save()
    return redirect('todo')
    # todo = Todo.objects.get(id = pk)
    # if todo.Is_finished ==True:
    #    todo.Is_finished = False
    # else:
    #  todo.Is_finished =True
    #  todo.save()
    # return redirect('todo')
    
def Books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        
        try:
            url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
            r = requests.get(url, timeout=10)
            r.raise_for_status()  # Raises an exception for bad status codes
            answer = r.json()
            
            result_list = []
            
            # Check if items exist in response
            if 'items' not in answer:
                messages.error(request, f"No books found for '{text}'")
                context = {'form': form, 'results': []}
                return render(request, 'dashboard/books.html', context)
            
            # Get available items (might be less than 10)
            items_count = min(len(answer['items']), 10)
            
            for i in range(items_count):
                item = answer['items'][i]
                volume_info = item.get('volumeInfo', {})
                
                # Handle thumbnail properly
                image_links = volume_info.get('imageLinks', {})
                thumbnail = image_links.get('thumbnail') if image_links else None
                
                result_dict = {
                    'title': volume_info.get('title', 'No Title'),
                    'subtitle': volume_info.get('subtitle', ''),
                    'description': volume_info.get('description', 'No description available'),
                    'count': volume_info.get('pageCount', 'Unknown'),
                    'categories': volume_info.get('categories', []),
                    'rating': volume_info.get('averageRating', 'No rating'),
                    'thumbnail': thumbnail,
                    'preview': volume_info.get('previewLink', ''),
                }
                result_list.append(result_dict)
            
            context = {'form': form, 'results': result_list}
            return render(request, 'dashboard/books.html', context)
            
        except requests.exceptions.RequestException as e:
            messages.error(request, "Error connecting to Google Books API")
            context = {'form': form, 'results': []}
            return render(request, 'dashboard/books.html', context)
        except KeyError as e:
            messages.error(request, f"Error processing book data: {str(e)}")
            context = {'form': form, 'results': []}
            return render(request, 'dashboard/books.html', context)
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            context = {'form': form, 'results': []}
            return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
        context = {'form': form, 'results': []}
        return render(request, 'dashboard/books.html', context)

# def dictionary(request):
#     if request.method == 'POST':
#         form = DashboardForm(request.POST)
#         text = request.POST['text']
#         url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
#         r = requests.get(url)
#         answer = r.json()
        
#         try:
#             phonetics= answer[0]['phonetics'][0]['text']
#             audio= answer[0]['phonetics'][0]['audio']
#             # print('audio',audio)
#             definition= answer[0]['meanings'][0]['definitions'][0]
#             examples= answer[0]['meanings'][0]['definitions'][0]['example']
#             synonyms= answer[0]['meanings'][0]['definitions'][0]['synonyms']
#             context={
#                 'form':form,
#                 'input':text,
#                 'phonetics':phonetics,
#                 'audio':audio,
#                 'definition':definition,
#                 'examples':examples,
#                 'synonyms':synonyms
                
#             }
#         except:
#             context={
#                 'form':form,
#                 'input':'',
#                 }
#         return render(request,'dashboard/dictionary.html',context)
#     else:
#        form = DashboardForm()
#        context = {'form':form}
#     return render(request,'dashboard/dictionary.html',context)


def dictionary(request):
    form = DashboardForm()
    context = {'form': form}

    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '').strip().lower()

        if text:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
            r = requests.get(url)

            if r.status_code == 200:
                try:
                    answer = r.json()
                    word_data = answer[0]
                    
                    # Extract phonetics and audio
                    phonetics = ''
                    audio = ''
                    if 'phonetics' in word_data and word_data['phonetics']:
                        for phonetic in word_data['phonetics']:
                            if phonetic.get('text'):
                                phonetics = phonetic['text']
                                break
                        for phonetic in word_data['phonetics']:
                            if phonetic.get('audio'):
                                audio = phonetic['audio']
                                break
                    
                    # Initialize collections for all meanings
                    all_definitions = []
                    all_examples = []
                    all_synonyms = set()
                    all_antonyms = set()
                    
                    # Extract from all meanings and definitions
                    if 'meanings' in word_data:
                        for meaning in word_data['meanings']:
                            if 'definitions' in meaning:
                                for definition_obj in meaning['definitions']:
                                    # Collect definitions
                                    if definition_obj.get('definition'):
                                        all_definitions.append(definition_obj['definition'])
                                    
                                    # Collect examples
                                    if definition_obj.get('example'):
                                        all_examples.append(definition_obj['example'])
                                    
                                    # Collect synonyms
                                    if definition_obj.get('synonyms'):
                                        all_synonyms.update(definition_obj['synonyms'])
                                    
                                    # Collect antonyms
                                    if definition_obj.get('antonyms'):
                                        all_antonyms.update(definition_obj['antonyms'])
                            
                            # Also check for synonyms/antonyms at meaning level
                            if meaning.get('synonyms'):
                                all_synonyms.update(meaning['synonyms'])
                            if meaning.get('antonyms'):
                                all_antonyms.update(meaning['antonyms'])
                    
                    # Prepare final data
                    primary_definition = all_definitions[0] if all_definitions else 'Definition not available.'
                    
                    # If no examples found, create a generic one
                    if not all_examples:
                        all_examples = [f"Please use '{text}' in a sentence."]
                    
                    # Convert sets to lists and limit to reasonable numbers
                    synonyms_list = list(all_synonyms)[:10]  # Limit to 10 synonyms
                    antonyms_list = list(all_antonyms)[:10]  # Limit to 10 antonyms
                    
                    # If no synonyms/antonyms found, you could optionally add fallback logic here
                    # or use a secondary API like WordsAPI or Merriam-Webster
                    
                    context.update({
                        'input': text,
                        'phonetics': phonetics,
                        'audio': audio,
                        'definition': primary_definition,
                        'examples': all_examples[0],  # Show first example
                        'all_examples': all_examples,  # In case you want to show multiple
                        'synonyms': synonyms_list,
                        'antonyms': antonyms_list,
                    })
                    
                except (KeyError, IndexError, TypeError) as e:
                    context['error'] = f"Could not parse dictionary response: {str(e)}"
            else:
                context['error'] = "Word not found or API limit exceeded."
        else:
            context['error'] = "Please enter a word to search."

    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        
        try:
            # Set language and configure wikipedia
            wikipedia.set_lang("en")
            
            # Search for the page
            search = wikipedia.page(text)
            
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary
            }
            return render(request, 'dashboard/wiki.html', context)
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Multiple pages found, use the first option
            try:
                search = wikipedia.page(e.options[0])
                context = {
                    'form': form,
                    'title': search.title,
                    'link': search.url,
                    'details': search.summary
                }
                return render(request, 'dashboard/wiki.html', context)
            except Exception:
                messages.error(request, f"Multiple articles found for '{text}'. Please be more specific.")
                context = {'form': form}
                return render(request, 'dashboard/wiki.html', context)
                
        except wikipedia.exceptions.PageError:
            messages.error(request, f"No Wikipedia page found for '{text}'")
            context = {'form': form}
            return render(request, 'dashboard/wiki.html', context)
            
        except Exception as e:
            messages.error(request, f"Error searching Wikipedia: {str(e)}")
            context = {'form': form}
            return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/wiki.html', context)
#     if request.method =="POST":
#         text=request.POST['text']
        
#         form=DashboardForm(request.POST)
#         search=wikipedia.page(text)
#         context={
#             'form' :form,
#             'title':search.title,
#             'link': search.url,
#             'details':search.summary
#         }
#         return render(request,'dashboard/wiki.html',context)
#     else:
#      form=DashboardForm()
#      context= {'form':form}
#     return render(request,'dashboard/wiki.html',context)

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
            messages.success(request,f"Welcome {username} Account Created for you Successfully!!")
            print(username)
        return redirect('login') 
        
    else:   
     form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'dashboard/register.html',context)



class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f"Welcome , {form.get_user().username}!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


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
     

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
    

# Add to your dashboard/views.py
from django.conf import settings
from django.db import connection

@csrf_exempt
def debug_database(request):
    try:
        db_config = settings.DATABASES['default']
        db_name = db_config.get('NAME', 'Unknown')
        db_engine = db_config.get('ENGINE', 'Unknown')
        
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            connection_status = "Connected successfully"
            
        # Check if we can see users table
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            user_count = cursor.fetchone()[0]
            
        return HttpResponse(f"""
        Database Engine: {db_engine}<br>
        Database Name: {db_name}<br>
        Connection: {connection_status}<br>
        User Count: {user_count}<br>
        Environment DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')[:50]}...
        """)
    except Exception as e:
        return HttpResponse(f"Database Error: {str(e)}")