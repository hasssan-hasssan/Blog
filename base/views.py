from django.shortcuts import render, get_object_or_404
from base.models import Post, Category, Review


def post_list(request, category = None):
    posts = []
    if category:
        category = get_object_or_404(Category, slug=category)
        posts = Post.published.all().filter(category = category).order_by('-publish')
    else:
        posts = Post.published.all().order_by('-publish')
    
    return render(request, 'list.html', {'posts': posts})


def post_detail(request, year, month, day ,slug):
    post = Post.published.get(publish__year=year, publish__month=month, publish__day=day, slug=slug)
    reviews = Review.confirmed.all().filter(post=post)
    
    return render(request, 'detail.html', {'post':post, 'reviews':reviews})
        
 
