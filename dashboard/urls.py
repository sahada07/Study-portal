from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('note', views.notes, name='notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete-note'),
    path('notes_detail/<int:pk>', views.NoteDetailView.as_view(), name='note-detail'),
    
    path('homework', views.homework, name='home-work'),
    path('update-homework/<int:pk>', views.update_homework, name='update-homework'),
    path('delete_work/<int:pk>', views.delete_work, name='delete-work'),
    
    path('youtube', views.youtube, name='youtube'),
    path('todo', views.todo, name='todo'),
    path('delete/<int:pk>', views.delete_todo, name='delete-todo'),
    path('update/<int:pk>', views.update_todo, name='update-todo'),
    
    path('books',views.Books,name='book'),
    path('dictionary',views.dictionary,name='dictionary'),
    path('wiki',views.wiki,name='wiki'),
    path('convert',views.Conversion,name='convert'),
    path('register',views.register,name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('run-migrations/', views.run_migrations, name='run_migrations'),
    path('debug-database/', views.debug_database, name='debug_database'),
    
] 


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


