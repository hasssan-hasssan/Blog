from django.db import models
from django.conf import settings
from django.utils import timezone
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    create = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name_plural = 'categories'
        

class Post(models.Model):
    STATUS_CHOICES = ((('draft', 'Draft'),('published', 'Published')))
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    body = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='posts', null=True)
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        
        
class Review(models.Model):
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    confirm = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    
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
  