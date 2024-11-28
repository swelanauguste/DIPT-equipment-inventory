import threading

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView, UpdateView
from users.models import User

from .forms import CustomPasswordResetForm, UserCustomCreationForm, UserUpdateForm
from .models import User
from .tasks import forgot_password_email, user_registration_email
from .tokens import account_activation_token


def reset_password_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been successfully reset.")
                return redirect("login")
        else:
            form = SetPasswordForm(user)
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect(
            "forgot-password"
        )  # Redirect to forgot password page if invalid link

    return render(request, "users/reset_password.html", {"form": form})


def forgot_password_view(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            reset_link = f"http://{domain}/users/reset-password/{uid}/{token}/"

            # Send email
            subject = "Password Reset Requested"
            message = render_to_string(
                "users/emails/password_reset_email.html",
                {
                    "user": user,
                    "reset_link": reset_link,
                },
            )
            forgot_password_email_thread = threading.Thread(
                target=forgot_password_email,
                args=(email, user, reset_link, message, subject),
            )
            forgot_password_email_thread.start()

            messages.success(
                request, "A password reset link has been sent to your email."
            )
            return redirect(
                "login"
            )  # Change to your login page or another appropriate page
    else:
        form = CustomPasswordResetForm()

    return render(request, "users/forgot_password.html", {"form": form})


class UserLoginView(auth_views.LoginView):
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


@login_required
def change_password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request, user
            )  # Prevent logout after password change
            messages.success(request, "Your password has been updated successfully!")
            return redirect(
                "change_password_done"
            )  # Replace with your own redirect URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "users/password_change.html", {"form": form})


from django.shortcuts import render


def password_change_done_view(request):
    return render(request, "users/password_change_done.html")


class UserPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "users/change_password_done.html"


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "users/password_reset.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("/")
    else:
        return redirect("login")


def user_registration_view(request):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    if request.method == "POST":
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_registration_email.after_response(
                request, user, form.cleaned_data["email"]
            )
            # user_registration_email(request, user, form.cleaned_data.get("email"))
            return redirect("login")
    else:
        form = UserCustomCreationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def user_update(request):
    user = get_object_or_404(User, slug=request.user.slug)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(
                "user-detail",
            )  # Redirect to a user detail or other page
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/user_form.html", {"form": form, "user": user})


@login_required
def user_detail(request):
    user = get_object_or_404(User, slug=request.user.slug)
    return render(request, "users/user_detail.html", {"user": user})


@login_required
def get_user_detail(request, slug):
    user = get_object_or_404(User, slug=slug)
    return render(request, "users/get_user_detail.html", {"user": user})
