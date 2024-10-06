from django.http import HttpResponse
from django.shortcuts import render


def custom_error_view(request, exception=None, template_name="error.html", status=500):
    """Vue générique pour les pages d'erreurs."""
    return render(request, template_name, status=status)


def custom_permission_denied_view(request, exception=None):
    return custom_error_view(
        request, exception, template_name="errors/403.html", status=403
    )


def custom_page_not_found_view(request, exception=None):
    return custom_error_view(
        request, exception, template_name="errors/404.html", status=404
    )


def custom_server_error_view(request):
    return custom_error_view(request, template_name="errors/500.html", status=500)


def cause_server_error(request):
    raise Exception("This is a test exception!")
