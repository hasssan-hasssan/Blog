from django.contrib import admin
from base.models import Post, Review, Reply, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create', 'status', 'category', 'tag_list', )
    list_filter = ('status', 'create', 'author')
    ordering = ('status', 'publish')
    date_hierarchy = 'create'
    search_fields = ('title__startswith',)
    prepopulated_fields = {"slug": ["title"]}
    
    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
  
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('report','create', 'confirm', )
    list_filter = ('confirm',)
    ordering = ('confirm',)
    
    def report(self,obj):
        return f"Comment on post [ {obj.post.title} ]"
    
   
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create')

