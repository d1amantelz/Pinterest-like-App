from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import *

main_menu = [{'name': 'Лента', 'alt': '', 'logo_src': 'website/logos/home-alt.svg', 'href': 'pins'},
             {'name': 'Коллекции', 'alt': '', 'logo_src': 'website/logos/folder.svg', 'href': 'collections'},
             {'name': 'Создать', 'alt': '', 'logo_src': 'website/logos/plus.svg', 'href': 'add_project'},
             {'name': 'Поиск', 'alt': '', 'logo_src': 'website/logos/search.svg', 'href': 'search'},
             ]
user_menu = [{'name': 'Войти', 'alt': '', 'logo_src': 'website/logos/log-in.svg', 'href': 'users:login'},
             {'name': 'Регистрация', 'alt': '', 'logo_src': 'website/logos/sign_up.svg', 'href': 'users:sign_up'}]


class MainPage(ListView):
    model = Pins
    template_name = 'website/pins.html'
    context_object_name = 'pins'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Лента'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


class ShowPin(DetailView):
    model = Pins
    template_name = 'website/pin.html'
    context_object_name = 'pin'
    pk_url_kwarg = 'pin_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['pin']
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


@method_decorator(login_required, name='dispatch')
class CollectionsPage(ListView):
    model = Collections
    template_name = 'website/collections.html'
    context_object_name = 'collections'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Коллекции'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context

    def get_queryset(self):
        return Collections.objects.filter(author=self.request.user.profile)


class ShowCollection(ListView):
    model = Collections
    template_name = 'website/collection.html'
    context_object_name = 'collection'
    pk_url_kwarg = 'collection_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['collection']
        context['pins'] = Pins.objects.filter(collection=self.kwargs['collection_id'],
                                              author=self.request.user.profile)
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context

    def get_queryset(self):
        return Collections.objects.get(pk=self.kwargs['collection_id'])


class AddProject(CreateView):
    form_class = AddProjectForm
    template_name = 'website/add_project.html'
    success_url = reverse_lazy('collections')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создание проекта'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


class ProfilePage(ListView):
    model = Profile
    template_name = 'website/profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'profile_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['profile']
        context['pins'] = Pins.objects.filter(author=context['profile']).annotate(count=Count('pk'))
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context

    def get_queryset(self):
        return Profile.objects.get(pk=self.kwargs['profile_id'])


class SearchPage(ListView):
    model = Pins
    template_name = 'website/search.html'
    context_object_name = 'pins'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Поиск'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context

    def post(self, request):
        search_term = request.POST.get('q')

        if search_term:
            pins = Pins.objects.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term))
        else:
            pins = Pins.objects.all()

        return render(request,
                      template_name='website/search_results.html',
                      context={
                          'query': search_term,
                          'pins': pins,
                          'main_menu': main_menu,
                          'user_menu': user_menu,
                          'page_title': 'Результаты поиска'})


class ChangeProfile(UpdateView):
    form_class = ChangeProfileForm
    template_name = 'website/change_profile.html'

    def get_success_url(self):
        profile_id = self.object.id
        return reverse_lazy('profile', kwargs={'profile_id': profile_id})

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Изменение профиля'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context
