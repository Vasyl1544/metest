from django.contrib import admin
from post.models import Post, Comment


class Post_Admin(admin.ModelAdmin):
    list_display = ('title', 'update', 'timestamp')
    list_filter = ('update', 'timestamp')
    list_editable = ('title', )
    list_display_links = ('update', )


admin.site.register(Post, Post_Admin)
admin.site.register(Comment)
