from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages


class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        user = self.request.user

        # Handle redirection based on user role
        if user.is_authenticated:
            if user.is_superuser:
                return self.get_redirect_url() or '/admin/'

        return '/'