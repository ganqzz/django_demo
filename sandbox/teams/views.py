from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, DetailView, \
    CreateView, UpdateView, DeleteView

from . import models


class HomeView(TemplateView):
    template_name = 'teams/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games_today'] = 6
        return context


class TeamListView(ListView):
    # template_name = 'teams/team_list.html'
    context_object_name = 'teams'  # default: 'object_list' or <lower_case_model_name>_list
    model = models.Team


class TeamListViewMixed(CreateView, ListView):  # mroに注意
    context_object_name = 'teams'
    fields = ('name', 'practice_location', 'coach')
    model = models.Team
    template_name = 'teams/team_list.html'


class TeamDetailView(DetailView):
    # template_name = 'teams/team_detail.html'
    # context_object_name = 'team'  # default: 'object' or <lower_case_model_name>
    model = models.Team


class TeamDetailViewMixed(UpdateView, DetailView):
    fields = ('name', 'practice_location', 'coach')
    model = models.Team
    template_name = 'teams/team_detail.html'


class PageTitleMixin:
    page_title = ''

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # mro
        context['page_title'] = self.get_page_title()
        return context


class TeamCreateView(LoginRequiredMixin, PageTitleMixin, CreateView):
    # template_name = 'teams/team_form.html'
    fields = ('name', 'practice_location', 'coach')
    model = models.Team
    page_title = 'Create a new team'

    def get_initial(self):
        initial = super().get_initial()
        initial['coach'] = self.request.user.pk
        return initial


class TeamUpdateView(LoginRequiredMixin, PageTitleMixin, UpdateView):
    # template_name = 'teams/team_form.html'
    fields = ('name', 'practice_location', 'coach')
    model = models.Team

    def get_page_title(self):
        obj = self.get_object()
        return 'Update {}'.format(obj.name)


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    # template_name = 'teams/team_confirm_delete.html'
    model = models.Team
    success_url = reverse_lazy('teams:list')

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(coach=self.request.user)  # 自分
        return self.model.objects.all()
