from django.contrib import admin
from .models import Comment, Post


# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for the Post model."""

    list_display = ('title', 'slug', 'author', 'publish', 'status')  # Displayed columns
    list_filter = ('status', 'created', 'publish', 'author')  # Sidebar filters
    search_fields = ('title', 'body')  # Searchable fields
    prepopulated_fields = {'slug': ('title',)}  # Auto-fill slug from title
    raw_id_fields = ('author',)  # Author field with lookup widget
    date_hierarchy = 'publish'  # Enables date-based navigation
    ordering = ('status', 'publish')  # Default sorting order

    # Django 5.0+ feature (Uncomment when upgrading)
    # show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
