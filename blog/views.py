from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            title__icontains=query
        ).order_by('-id')
    else:
        posts = Post.objects.all().order_by('-id')

    return render(
        request,
        'home.html',
        {'posts': posts}
    )

@login_required
def post_detail(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        content = request.POST.get('comment')
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments
    })

@login_required
def add_post(request):
    if request.method=="POST":
        title=request.POST.get('title')
        content=request.POST.get('area')
        if title and content:
            Post.objects.create(user=request.user,title=title,content=content)
            return redirect('/')
    return render(request,'add_post.html')

@login_required
def delete(request,id):
    post=Post.objects.get(id=id)
    
    if post.user != request.user:
        return redirect('/') 
    
    if request.method=='POST':
        post.delete()
        return redirect('/')
    return render(request,'delete_confirm.html',{'post':post})

@login_required
def edit(request,id):
    post=Post.objects.get(id=id)
    
    if post.user != request.user:
        return redirect('/') 
    
    if request.method=="POST":
        title=request.POST.get('title')
        content=request.POST.get('area')
        
        if title and content:
            post.title=title
            post.content=content
            post.save()
        return redirect('/')
    return render(request,'edit_post.html',{'post':post})


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return redirect('/')
        else:
            return render(request,'login_page.html',{'error':'invaild credentials'})
    return render(request,'login_page.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def user_profile(request, username):
    profile_user = User.objects.get(username=username)
    posts = Post.objects.filter(user=profile_user)

    return render(request, 'user_profile.html', {
        'profile_user': profile_user,
        'posts': posts
    })


@login_required
def like_post(request, id):
    post = Post.objects.get(id=id)
    #already liked?
    if request.user in post.likes.all():
        # unlike
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('/')
