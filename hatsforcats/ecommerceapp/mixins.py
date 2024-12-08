from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

class GroupRequiredMixin(AccessMixin):
    """
    Custom Mixin to check if the user is authenticated and belongs to a required group.
    Redirects unauthenticated users to the login page and unauthorized users to an unauthorized page.
    """

    group_required = None  # Specify the required group as a string

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = f"{reverse('login')}?next={request.path}" # send to login page and then send them back after
            return HttpResponseRedirect(login_url)

        if self.group_required and not request.user.groups.filter(name=self.group_required).exists():
            return redirect('unauthorized') 

        return super().dispatch(request, *args, **kwargs)