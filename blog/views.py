from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list (request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #Three post en each page
    page = request.GET.get('page')
    try: 
        posts = paginator.page(page)
    except PageNotAnInteger:
        #IF the page is not an integer, deliver the frist page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {'posts':posts}
    return render(request, 'blog/post/list.html', context) # takes the request object, the emplate path, and the context variables to render the given template

def post_detail(request, year, month, day, post): #retrieves the object that matches the given arameters or an HTTP 404 (not found) exception if no object is found. 
    post = get_object_or_404(Post, slug=post, status='published', publish__year = year, publish__month = month, publish__day = day) 
    context = {'post':post}
    return render(request, 'blog/post/detail.html', context)

