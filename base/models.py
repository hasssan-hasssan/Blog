from django.db import models
from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from base.managers import *


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    create = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name_plural = 'categories'
        

class Post(models.Model):
    thumbnail = models.ImageField(null=True, blank=True, upload_to='photos/posts/')
    STATUS_CHOICES = ((('draft', 'Draft'),('published', 'Published')))
    title = models.CharField(max_length=200)
    intro = models.CharField(max_length=255, default="")
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    body = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='posts', null=True)
    tags = TaggableManager()
    objects = models.Manager() # Django manager
    published = PublishedManager() # Custom manager for fetch published posts
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("post_detail", args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug,
        ])
    
        
        
class Review(models.Model):
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    confirm = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    objects = models.Manager() # Django manager
    confirmed = ConfirmReviewManager() # Custom manager for fetch confirm reviews.
    
    def __str__(self):
        return f"{self.text[:30]} on Post: {str(self.post.title)}"
    

class Reply(models.Model):
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply')
    
    def __str__(self):
        return f"Answer {str(self.user.username)} to review [{str(self.review.id)}] on post [{str(self.review.post.id)}]"
    
    class Meta:
        verbose_name_plural = 'replies'
  