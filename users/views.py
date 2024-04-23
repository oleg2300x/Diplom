from random import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserForm
from users.models import User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


class ProfileView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def generate_password(request):
    """
      Сброс пароля
      """
    if request.method == 'POST':
        email = request.POST.get('user_email')
        try:
            user = User.objects.get(email=email)
            new_password = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            send_mail(
                subject='New password',
                message=f'Your new password {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            user.set_password(new_password)
            user.save()
            return redirect(reverse('login'))
        except Exception:
            message = 'We can not find user with this email'
            context = {
                'message': message
            }
            return render(request, 'users/forgot_password.html', context)
    else:
        return render(request, 'users/forgot_password.html')
