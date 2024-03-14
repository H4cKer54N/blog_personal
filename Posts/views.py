from datetime import datetime, timedelta, timezone
from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView,ListView, DetailView
from .decorators import add_dropdowns_to_context
from django.utils.decorators import method_decorator
from .models import ContactForm, Post, Tags
from django.db.models import Count

@method_decorator(add_dropdowns_to_context, name='get_context_data')
class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Inicio"
        context["title_window"] = "Inicio"
        context["trending"] = Post.objects.filter(trending=True).order_by('-date_posted')[:5]
        context["posts_por_tag"] = self.obtener_posts_por_tag()
        context["hero"] = Post.objects.filter(hero=True).order_by('-date_posted')
        return context
    
    def get_queryset(self):
        return Post.objects.all().order_by('-date_posted')

    def obtener_posts_por_tag(self):
        tags_populares = Tags.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:3]
        resultados = []
        for tag in tags_populares:
            posts_recientes = tag.post_set.all().order_by('-date_posted')[:5]
            resultados.append({
                'tag': tag,
                'posts': posts_recientes
            })
        return resultados

@method_decorator(add_dropdowns_to_context, name='get_context_data')
class SearchByTag(ListView):
    template_name = 'category.html'
    model = Post

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = f"Categoría : {self.kwargs['str']}"
        context["title_window"] = f"{self.kwargs['str']}"
        return context
    
    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs['str'])


@method_decorator(add_dropdowns_to_context, name='get_context_data')
class SearchByUser(ListView):
    template_name = 'category.html'
    model = Post

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = f"Usuario : {self.kwargs['str']}"
        context["title_window"] = f"{self.kwargs['str']}"

        return context
    
    def get_queryset(self):
        return Post.objects.filter(author__username=self.kwargs['str'])

@method_decorator(add_dropdowns_to_context, name='get_context_data')
class DetailViewPost(DetailView):
    template_name = 'single-post.html'
    model = Post

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["title_window"] = self.object.title
        return context
    
@method_decorator(add_dropdowns_to_context, name='get_context_data')
class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Contacto"
        context["title_window"] = "Contacto"
        return context
    
    def post(self, request, *args: Any, **kwargs: Any) -> Any:
        if request.POST['name'] == "" or request.POST['email'] == "" or request.POST['subject'] == "" or request.POST['message'] == "":
            return render(request, 'contact.html', {'title': 'Contacto', 'title_window': 'Contacto', "status":"400",'message': 'Por favor, rellene todos los campos'})
        time_last_message = ContactForm.objects.filter(email=request.POST['email']).order_by('-date_posted').first()
        time_last_message_date_posted_aware = time_last_message.date_posted.replace(tzinfo=timezone.utc)
        diferencia_de_tiempo = datetime.now(timezone.utc) - time_last_message_date_posted_aware
        sec_30 = timedelta(seconds=30)

        if diferencia_de_tiempo < sec_30:
                return render(request, 'contact.html', {'title': 'Contacto', 'title_window': 'Contacto', "status":"400",'message': 'No puedes enviar más de un mensaje cada 30 segundos'})

        ContactForm.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        print(request.POST)
        return render(request, 'contact.html', {'title': 'Contacto', 'title_window': 'Contacto', "status":"200",'message': 'Mensaje enviado con éxito'})