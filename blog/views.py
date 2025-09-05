from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "blogposts"

    def get_queryset(self):
        # Выводим только опубликованные статьи
        return super().get_queryset().filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "blogpost"

    def get_object(self, queryset=None):
        # Увеличиваем счетчик просмотров
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:blogpost_list")


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def get_success_url(self):
        # Перенаправляем на страницу статьи после редактирования
        return reverse_lazy("blog:blogpost_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:blogpost_list")
