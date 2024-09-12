"""
URL configuration for auto_qcm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.contrib.auth import views as auth_views
from app.views import (
    QuestionListView,
    create_or_edit_question,
    remove_tag,
    delete_question,
    home,
    CustomLoginView,
    export_question_xml,
    support_doc,
    etudiant_dashboard,
    QcmListView, 
    create_qcm,
    enseignant_dashboard,
    search_student,
    delete_qcm,
    export_qcm_xml
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("list-questions/", QuestionListView.as_view(), name="question-list"),
    path('question/create/', create_or_edit_question, name='create-question'),
    path('question/edit/<int:pk>/', create_or_edit_question, name='edit-question'),
    path('etudiant-dashboard/<int:pk>/', etudiant_dashboard, name="etudiant-dashboard"),
    path('enseignant-dashboard/<int:pk>/', enseignant_dashboard, name="enseignant-dashboard"),
    path("support-doc/", support_doc, name="support-doc"),
    path("remove-tag/<int:question_id>/<int:tag_id>/", remove_tag, name="remove-tag"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("delete-question/<int:question_id>/", delete_question, name="delete-question"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "export-question/<int:question_id>/",
        export_question_xml,
        name="export-question",
    ),
    path('create-qcm/',create_qcm, name="qcm-create"),
    path('list-qcm/',QcmListView.as_view(),name='qcm-list'),
    path('search-student/', search_student, name='search-student'),
    path('delete-qcm/<int:qcm_id>/',delete_qcm,name="delete-qcm"),
    path('export-qcm-xml/<int:qcm_id>/',export_qcm_xml,name="export-qcm-xml")
]

if os.environ.get("env", "dev") == "dev":
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
