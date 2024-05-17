"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', ReactView.as_view(), name="anything"),
    path('user/login', UserView.as_view(), name="anything"),
    path('reader/login', ReaderLoginView.as_view(), name="anything"),
    path('reader/register', ReaderRegisterView.as_view(), name="anything"),
    path('reader/change-password/', ReaderChangePasswordView.as_view(), name='change-password'),
    
    path('books', BookView.as_view(), name="anything"),
    path('books/popular/', BookByPopularView.as_view(), name='book-popular-list'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('books/content/<int:book_id>/<int:page_number>', BookContentView.as_view(), name="anything"),
    path('books/upload/<int:book_id>/<str:fileName>', BookUploading, name='book_upload'),
    path('books/search/', BookSearchView.as_view(), name='book-search'),
    
    
    path('shelf/', ShelfView.as_view(), name='shelf-list'),  
    path('shelf/<int:user_id>/', ShelfView.as_view(), name='shelf-by-user'),  # For retrieving shelves by user ID
    path('shelf/delete/<int:shelf_id>/', ShelfView.as_view(), name='delete-shelf'),
    path('shelves-containing-book/<int:user_id>/<int:book_id>/', ShelvesContainingBookView.as_view(), name='shelves-containing-book'),
   
    path('addedbooks/', AddedBookView.as_view(), name='addedbook-list'),  # For creating a new added book
    path('addedbooks/<int:user_id>/<int:shelf_id>/', AddedBookView.as_view(), name='shelf-by-user'),  # For retrieving shelves by user ID
    path('addedbook/delete/<int:shelf_id>/<int:user_id>/<int:book_id>/', AddedBookView.as_view(), name='delete-addedbook'),
    
    path('audiofolders/', AudioFolderView.as_view(), name='audio_folder_list'),
    path('audiofolders/<int:user_id>/', AudioFolderView.as_view(), name='user_audio_folder_list'),
    path('audiofolder/delete/<int:audio_folder_id>/', DeleteAudioFolderView.as_view(), name='delete-audiofolder'),
    
    path('audiofiles/', AudioFileView.as_view(), name='audio_file_list'),
    path('audiofiles/<int:user_id>/', AudioFileView.as_view(), name='user_audio_file_list'),
    path('audiofiles/<int:user_id>/<int:folder_id>/', AudioFileView.as_view(), name='user_folder_audio_file_list'),
    path('audiofile/delete/<int:audio_file_id>/', DeleteAudioFileView.as_view(), name='delete-audiofile'),
    
    path('ratings/', RatingView.as_view(), name='rating_list'),  # For creating or updating a rating
    path('ratings/<int:user_id>/<int:book_id>/', RatingView.as_view(), name='user_book_rating'),  # For retrieving a rating
    
    #path('readerInfo/', ReaderInfoCreateView.as_view(), name='reader_info'),
    path('readerinfo/email/<str:email>/', ReaderInfoByEmailView.as_view(), name='readerinfo_by_email'),
    path('readerinfo/id/<int:reader_id>/', ReaderInfoByIdView.as_view(), name='readerinfo_by_id'),
    path('readerinfo/', ReaderChangeInfo.as_view(), name='change_reader_info'),
    
    path('readingprocess/', ReadingProcessView.as_view(), name='reading-process'),
    path('readingprocess/<int:user_id>/<int:book_id>/', ReadingProcessView.as_view(), name='reading-process-detail'),
    path('readingprocess/recentbook/<int:user_id>/', RecentBookAPI.as_view(), name='reading-process-detail'),
    
]
    # path('Path', getPathOS, name='getPathOS'),
