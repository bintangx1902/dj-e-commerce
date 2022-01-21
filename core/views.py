from django.shortcuts import render
from django.views.generic import *
from .forms import *

item_slug = 'item_slug'
bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '&', '(', ')']


def bad_chars_check(link: str):
    if bad_chars[-3] in link:
        link = link.replace(bad_chars[-3], 'n')

    for x in bad_chars:
        link = link.replace(x, '')

    while True:
        if link[-1] == '-':
            link = link[:-1]
        else:
            break

    return link


class HomeLandingView(ListView):
    model = Item
    paginate_by = 10
    ordering = ['-id']
    template_name = 'core/item_list.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = ''
    query_pk_and_slug = True
    slug_field = item_slug
    slug_url_kwarg = item_slug


class CreateItemViews(CreateView):
    template_name = "core/forms.html"
    model = Item
    form_class = CreateItemForms

    def get_success_url(self):
        return

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
    form_class = None
    template_name = None

    def get_success_url(self):
        return
