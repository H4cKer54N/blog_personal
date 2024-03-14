from functools import wraps
from .models import Tags, Post

def add_dropdowns_to_context(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        dropdowns_list = Tags.objects.all().order_by('name')
        last_5 = Post.objects.all().order_by('-date_posted')[:5]
        context = view_func(*args, **kwargs)

        context['dropdowns'] = dropdowns_list
        context['last_5'] = last_5

        return context

    return _wrapped_view

