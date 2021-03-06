from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.account.views import EmailView

from the_voice.performances.models import Team
from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.filter(
            status=Team.STATUS.active,
            mentors__pk=self.object.pk
        )
        print(context)
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse(
            'users:detail',
            kwargs={'username': self.request.user.username}
        )


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse(
            'users:detail',
            kwargs={'username': self.request.user.username}
        )

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserEmailView(LoginRequiredMixin, EmailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user
        return context



