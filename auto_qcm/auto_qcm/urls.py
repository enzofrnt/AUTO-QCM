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
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect  
from app.views import QuestionListView, QuestionCreateView, remove_tag, CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list-questions/', QuestionListView.as_view(), name='question-list'),
    path('create-questions/', QuestionCreateView.as_view(), name='question-create'),
    path('remove-tag/<int:question_id>/<int:tag_id>/', remove_tag, name='remove-tag'),
    path('login/', CustomLoginView.as_view(), name='login') , 
    
]
