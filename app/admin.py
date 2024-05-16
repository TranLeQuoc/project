from django.contrib import admin
from .models import *

admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(Shelf)
admin.site.register(AddedBook)
admin.site.register(AudioFolder)
admin.site.register(AudioFile)
admin.site.register(ReaderInfo)
admin.site.register(Rating)

# Register your models here.
