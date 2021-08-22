from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from .form import CreateUserForm, LoginForm
from django.views.generic import RedirectView, CreateView, ListView, DetailView, DeleteView, UpdateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from profiles.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from iface import settings
from .utils import generate_token

class CustomLoginView(LoginView):
    template_name = 'main_page.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post:home')
        return super(CustomLoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', False)
        if not remember_me:
            self.request.session.set_expiry(60 * 60) # 1 hour
        return super(CustomLoginView, self).form_valid(form)


class CustomRegisterView(CreateView):
    form_class = CreateUserForm
    template_name = 'register.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('post:home')
        else:
            return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('post:home')
        form = self.form_class(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            user_form = form.save(commit=False)
            same_email_user = User.objects.filter(email=user_form.email, is_active=True).exists()
            user = None
            if not same_email_user:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # send email
                mail_subject = force_text(_("Activate your account.")).strip()
                html_message = render_to_string('activate.html', {
                    'full_name': user.get_full_name(),
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                plain_message = strip_tags(html_message).strip()
                to_email = form.cleaned_data.get('email')
                send_mail(mail_subject, plain_message, "Friendly <admin@friendly.com>", [to_email],
                          html_message=html_message)
                return render(request, "info.html",
                              {"data": _("Please confirm your email address to complete the registration")})
            else:
                form.add_error("email", _("User with this email already exists!"))
            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form, 'title': _('Become a member')})


    def get_success_url(self):
        return reverse_lazy('authenticate:main_page')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        User.objects.filter(email=user.email, is_active=False).delete()
        login(request, user)
        return render(request, "info.html",
                      {"data": _("Thank you for your email confirmation. Now you can start using your account."),
                       "redirect_page": redirect("authenticate:main_page")})
    else:
        return render(request, "info.html", {"data": _("Activation link is invalid!")})











    
