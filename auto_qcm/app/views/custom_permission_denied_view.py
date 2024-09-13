from django.shortcuts import render
from django.http import HttpResponseForbidden

def custom_permission_denied_view(request, exception=None):
    return render(request, 'custompermission/403.html', status=403)
