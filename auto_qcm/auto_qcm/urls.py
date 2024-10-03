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

from app.views import (
    CustomLoginView,
    QcmListView,
    QuestionListView,
    change_password_view,
    corriger_qcm,
    create_or_edit_qcm,
    create_or_edit_question,
    custom_admin_view,
    delete_multiple_qcms,
    delete_qcm,
    delete_question,
    enseignant_dashboard,
    etudiant_dashboard,
    export_qcm_latex,
    export_qcm_xml,
    export_question_xml,
    home,
    qcm_responses,
    qcm_statistics,
    question_generation_view,
    remove_tag,
    repondre_qcm,
    save_generated_questions,
    search_student,
    support_doc,
    acces_qcm,
)
from django.conf.urls import handler403, handler404, handler500
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("", home, name="home"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("password_change/", change_password_view, name="password_change"),
    path("admin-dashboard/", custom_admin_view, name="admin-dashboard"),
    path(
        "password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="login.html"),
        name="password_change_done",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("support-doc/", support_doc, name="support-doc"),
    path("remove-tag/<int:question_id>/<int:tag_id>/", remove_tag, name="remove-tag"),
    # CRUD QUESTIONS
    path("question/list/", QuestionListView.as_view(), name="question-list"),
    path("question/create/", create_or_edit_question, name="question-create"),
    path("question/edit/<int:pk>/", create_or_edit_question, name="question-edit"),
    path("question/delete/<int:question_id>/", delete_question, name="question-delete"),
    path("question/generation/", question_generation_view, name="generate-questions"),
    path("save-questions/", save_generated_questions, name="save-questions"),
    # DASHBOARD
    path("etudiant-dashboard/<int:pk>/", etudiant_dashboard, name="etudiant-dashboard"),
    path(
        "enseignant-dashboard/<int:pk>/",
        enseignant_dashboard,
        name="enseignant-dashboard",
    ),
    path("search-student/", search_student, name="search-student"),
    path("qcm/responses/<int:qcm_id>/", qcm_responses, name="qcm-responses"),
    path("qcm/statistiques/<int:pk>/", qcm_statistics, name="qcm-statistics"),
    # CRUD QCM
    path("qcm/create/", create_or_edit_qcm, name="qcm-create"),
    path("qcm/edit/<int:pk>/", create_or_edit_qcm, name="qcm-edit"),
    path("qcm/list/", QcmListView.as_view(), name="qcm-list"),
    path("qcm/delete/<int:qcm_id>/", delete_qcm, name="qcm-delete"),
    # Reponse QCM
    path("qcm/acces/<int:qcm_id>/", acces_qcm, name="qcm-acces"),
    path("qcm/anwser/<int:qcm_id>/<int:rep_id>", repondre_qcm, name="qcm-answer"),
    path("qcm/correct/<int:repqcm_id>/", corriger_qcm, name="qcm-correct"),
    path("delete-multiple/", delete_multiple_qcms, name="qcm-delete-multiple"),
    # Export
    path(
        "question/export-xml/<int:question_id>/",
        export_question_xml,
        name="question-export-xml",
    ),
    path("qcm/export-xml/<int:qcm_id>/", export_qcm_xml, name="qcm-export-xml"),
    path("qcm/export-latex/<int:qcm_id>/", export_qcm_latex, name="qcm-export-latex"),
]

if os.environ.get("env", "dev") == "dev":
    urlpatterns.append(path("admin/", admin.site.urls))
    urlpatterns.append(
        path("__reload__/", include("django_browser_reload.urls"), name="reload")
    )

handler403 = "app.views.custom_error_view.custom_permission_denied_view"
handler404 = "app.views.custom_error_view.custom_page_not_found_view"
handler500 = "app.views.custom_error_view.custom_server_error_view"
