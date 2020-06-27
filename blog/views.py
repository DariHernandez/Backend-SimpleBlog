from django.shortcuts import render, get_list_or_404
from .models import Post

def post_list (request):
    post = Post.published.all() #Query-
    context = {'post':post}
    return render(request, 'blog/post/list.html', context) # takes the request object, the emplate path, and the context variables to render the given template

def post_detail(request, year, month, day, post): #retrieves the object that matches the given arameters or an HTTP 404 (not found) exception if no object is found. 
    post = get_object_or_404(Post, slug=post, 
                                status='published',
                                published__year = year
                                published__month = month
                                published__day = day) 
    context = {'post':post}
    return render(request, 'blog/post/details.html', context)

