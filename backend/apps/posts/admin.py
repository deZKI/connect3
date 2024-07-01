from django.contrib import admin

from apps.posts.models import Posts, PostsFiles, PostsDelivered


class PostsFilesInlineAdmin(admin.TabularInline):
    model = PostsFiles


class PostsDeliveredInlineAdmin(admin.TabularInline):
    model = PostsDelivered


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [PostsFilesInlineAdmin, PostsDeliveredInlineAdmin]
