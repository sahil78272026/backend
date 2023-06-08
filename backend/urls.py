# import from django
from django.contrib import admin
from django.urls import path,include

# Local Import
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stuinfo/<int:pk>', views.student_detail),
    path('stuinfo/', views.student_list),
    path('stucreate/',views.student_create),
    path('studentapi/',views.student_api),
    path('studentapicls/', views.StudentApi.as_view()) # for class based request
]
