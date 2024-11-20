from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class GroupRequiredMixin(AccessMixin):
    '''Custom Mixin to check if the user is authenticated and redirect them if not'''

    group_required = None  #String to specify the name of the group when we add the mixin to the class

    def dispatch(self, request, *args, **kwargs):
        '''Function to check for user permission and redirect is specified permission is not valid.'''
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.group_required and not request.user.groups.filter(name=self.group_required).exists():
            return redirect('login')  #Placeholder until we have created the login page
        return super().dispatch(request, *args, **kwargs)
