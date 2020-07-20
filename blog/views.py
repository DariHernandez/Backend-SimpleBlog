from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

def post_share(request, post_id):
    #Retrive port y id
    post = get_object_or_404(Post, id = post_id, status='published')
    sent = False

    if request.method == 'POST':
        #form we submited
        form = EmailPostForm(request.POST)
        if form.is_valid(): 
            #Form fields passes validation
            cd = form.cleaned_data
            post_url =  request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']}\'s comments: {cd ['comments']}"
            send_mail (subject, message, 'cidentymx@gmail.com',[cd['to']])
            sent = True
    else :
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form': form, 'sent':sent}) 

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
    post = get_object_or_404(Post, 
                            slug=post, status='published', 
                            publish__year = year, 
                            publish__month = month, 
                            publish__day = day) 

    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'post':post, 
                'comments':comments, 
                'new_comments':new_comment, 
                'comment_form':comment_form}
    return render(request, 'blog/post/detail.html', context)

class PostListView(ListView): 
    queryset = Post.published.all()
    context_object_name = 'posts' #Use the context variable posts for the query results. 
    paginate_by = 3 #Paginate the result, displaying three objects per page
    template_name = 'blog/post/list.html' #Use a custom template to render the page. If you don't set a default template


