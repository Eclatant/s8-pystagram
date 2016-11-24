from django.contrib import admin

# Register your models here.
from .models import Post
from .models import Comment


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'created_at', )
    list_display_links = ('id', 'created_at', )
    ordering = ('id', '-created_at', )
    inlines = (CommentInlineAdmin, )
    search_fields = ('id', 'content', )
    list_filter = ('category', 'tags', )
    date_hierarchy = 'created_at'


admin.site.register(Post, PostAdmin)
#admin.site.register(Comment)

