from django.contrib import admin

from .models import *


class PostImageInline(admin.TabularInline):
    model = PostImage
    max_num = 8
    min_num = 2


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ]


admin.site.register(Category)
admin.site.register(Rating)
