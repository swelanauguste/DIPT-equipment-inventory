from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class UserAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.role != "user"

    def handle_no_permission(self):
        messages.info(self.request, "Your request could not be completed.")
        if self.request.user.is_authenticated:
            return redirect("get-user-detail", slug=self.request.user.slug)
        return redirect("login")
