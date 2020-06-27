from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list (request):
    posts = Post.published.all() #Query-
    context = {'posts':posts}
    return render(request, 'blog/post/list.html', context) # takes the request object, the emplate path, and the context variables to render the given template

def post_detail(request, year, month, day, post): #retrieves the object that matches the given arameters or an HTTP 404 (not found) exception if no object is found. 
    post = get_object_or_404(Post, slug=post, status='published', publish__year = year, publish__month = month, publish__day = day) 
    context = {'post':post}
    return render(request, 'blog/post/detail.html', context)

