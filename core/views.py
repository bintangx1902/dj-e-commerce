from django.shortcuts import render, reverse, redirect
from django.views.generic import *
from .forms import *
from django.http import HttpResponseRedirect

item_slug = 'item_slug'
bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '&', '(', ')']


def bad_chars_check(link: str):
    link_ = link
    if bad_chars[-3] in link_:
        link_ = link_.replace(bad_chars[-3], 'n')

    for x in bad_chars:
        link_ = link_.replace(x, '')

    while True:
        if link_[-1] == '-':
            link_ = link_[:-1]
        else:
            break

    return link_


class HomeLandingView(ListView):
    model = Item
    paginate_by = 10
    ordering = ['-id']
    context_object_name = 'items'
    template_name = 'core/item_list.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/item_detail.html'
    query_pk_and_slug = True
    slug_field = item_slug
    slug_url_kwarg = item_slug


class CreateItemViews(CreateView):
    template_name = "core/forms.html"
    model = Item
    form_class = CreateItemForms

    def get_success_url(self):
        return reverse('core:home')

    def form_valid(self, form):
        link: str = form.cleaned_data['title']
        link = link.lower().replace(' ', '-')
        link = bad_chars_check(link)

        form.instance.item_slug = link
        return super(CreateItemViews, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateItemViews, self).get_context_data(**kwargs)
        context['title'] = "Create Item"
        return context


class UpdateItemViews(UpdateView):
    model = Item
    query_pk_and_slug = True
    slug_field = item_slug
    slug_url_kwarg = item_slug
    form_class = UpdateItemForms
    template_name = 'core/forms.html'

    def get_success_url(self):
        return reverse('core:item-update', kwargs={'item_slug': self.kwargs['item_slug']})

    def get_context_data(self, **kwargs):
        context = super(UpdateItemViews, self).get_context_data(**kwargs)
        context['title'] = 'Update'
        return context


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'core/forms.html'
    query_pk_and_slug = True
    slug_url_kwarg = item_slug
    slug_field = item_slug

    def get_success_url(self):
        return reverse('core:home')

    def get_context_data(self, **kwargs):
        context = super(ItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Item "
        context['delete'] = True
        return context
