from django.contrib import admin
from django.contrib import messages
from .models import Post


@admin.action(description="Approve selected posts")
def approve_posts(modeladmin, request, queryset):
    updated = queryset.update(status=Post.Status.APPROVED)
    modeladmin.message_user(
        request,
        f"{updated} post(s) approved.",
        level=messages.SUCCESS
    )


@admin.action(description="Reject selected posts")
def reject_posts(modeladmin, request, queryset):
    updated = queryset.update(status=Post.Status.REJECTED)
    modeladmin.message_user(
        request,
        f"{updated} post(s) rejected.",
        level=messages.WARNING
    )


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content', 'author__email', 'author__username')
    actions = [approve_posts, reject_posts]
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Post, PostAdmin)