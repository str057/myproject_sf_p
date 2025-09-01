from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from .forms import ProdForm, ParentForm
from .models import Product, Parent


class ProdListView(ListView):
    model = Product
    template_name = 'fly/product_list.html'
    context_object_name = 'products'


class ProdDetailView(DetailView):
    model = Product
    template_name = 'fly/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProdCreateView(CreateView):
    model = Product
    form_class = ProdForm
    success_url = reverse_lazy('fly:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ParentFormSet = inlineformset_factory(Product, Parent, form=ParentForm, extra=1, can_delete=True)
        if self.request.method == 'POST':
            context['formset'] = ParentFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = ParentFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProdUpdateView(UpdateView):
    model = Product
    form_class = ProdForm
    template_name = 'fly/product_form.html'

    def get_success_url(self):
        return reverse_lazy('fly:product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ParentFormSet = inlineformset_factory(Product, Parent, form=ParentForm, extra=1, can_delete=True)

        if self.request.method == 'POST':
            context['formset'] = ParentFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = ParentFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            # Если форма невалидна, возвращаем ошибки
            return self.render_to_response(self.get_context_data(form=form))


class ProdDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('fly:product_list')