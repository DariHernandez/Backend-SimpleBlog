from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin): #Class who  include information about how to display the model in the site and how to interact with it.
    list_display = ('title','slug','author','publish','status') #set the fields of your model that you want to display on the administration object list page. 
    list_filter = ('status', 'created', 'publish', 'author') #Add filters
    search_fields = ('title','body') #Search top bar
    prepopulated_fields = {'slug':('title',)} #automatically generate the value for slug
    raw_id_fields = ('author',) #hows a magnifying glass button next to the field which allows users to search for and select a value:
    date_hierarchy = 'publish' #Crete a herarcy/date filter
    ordering = ('status', 'publish') #Order