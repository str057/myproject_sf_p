from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .forms import ProdForm, ParentForm, FlyModeratorForm
from .models import Product, Parent


class ProdListView(ListView):
    model = Product
    template_name = "fly/product_list.html"
    context_object_name = "products"


class ProdDetailView(DetailView):
    model = Product
    template_name = "fly/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProdCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProdForm
    success_url = reverse_lazy("fly:product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ParentFormSet = inlineformset_factory(
            Product, Parent, form=ParentForm, extra=1, can_delete=True
        )
        if self.request.method == "POST":
            context["formset"] = ParentFormSet(self.request.POST, self.request.FILES)
        else:
            context["formset"] = ParentFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            # АВТОМАТИЧЕСКИ ЗАПОЛНЯЕМ ВЛАДЕЛЬЦА (ЗАДАНИЕ 2)
            form.instance.owner = self.request.user
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProdForm
    template_name = "fly/product_form.html"

    def test_func(self):
        """Проверка прав на редактирование (ЗАДАНИЕ 2)"""
        product = self.get_object()

        return product.owner == self.request.user

    def get_success_url(self):
        return reverse_lazy("fly:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ParentFormSet = inlineformset_factory(
            Product, Parent, form=ParentForm, extra=1, can_delete=True
        )

        if self.request.method == "POST":
            context["formset"] = ParentFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["formset"] = ParentFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:

            return self.render_to_response(self.get_context_data(form=form))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProdForm
        if user.has_perm("fly.can_edit_breed") and user.has_perm(
            "fly.can_edit_description"
        ):
            return FlyModeratorForm
        raise PermissionDenied


class ProdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("fly:product_list")

    def test_func(self):
        """Проверка прав на удаление (ЗАДАНИЕ 2)"""
        product = self.get_object()

        return (
            product.owner == self.request.user
            or self.request.user.groups.filter(name="Модератор продуктов").exists()
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Продукт успешно удален")
        return super().delete(request, *args, **kwargs)


class ProductPublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Product
    fields = []  # Не нужно менять поля, только статус
    template_name = "fly/product_confirm_publish.html"

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

    def form_valid(self, form):
        form.instance.publication_status = Product.PublicationStatus.PUBLISHED
        messages.success(self.request, "Продукт опубликован")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("fly:product_detail", kwargs={"pk": self.object.pk})


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Product
    fields = []
    template_name = "fly/product_confirm_unpublish.html"

    def test_func(self):
        product = self.get_object()

        return (
            self.request.user.has_perm("fly.can_unpublish_product")
            or product.owner == self.request.user
            or self.request.user.groups.filter(name="Модератор продуктов").exists()
        )

    def form_valid(self, form):
        form.instance.publication_status = Product.PublicationStatus.DRAFT
        messages.success(self.request, "Публикация продукта отменена")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("fly:product_detail", kwargs={"pk": self.object.pk})
