# import from django
from django.contrib import admin
from django.urls import path,include

# Local Import
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    # Function based View Practice
    path('stuinfo/<int:pk>', views.student_detail),
    path('stuinfo/', views.student_list),

    # Function based View Routers
    path('stucreate/',views.student_create),

     # Class based View Routers
    path('studentapicls/', views.StudentApi.as_view()), # for class based request

    # function based api_view
    path('student_api_with_view/', views.student_api_with_view),
    path('student_api_with_view/<int:pk>', views.student_api_with_view),

    # class based api_view
    path('classbasedstudent_api_with_view/', views.ClassBasedAPIViewStudentAPI.as_view()),
    path('classbasedstudent_api_with_view/<int:pk>', views.ClassBasedAPIViewStudentAPI.as_view()),

    # cloth API View
    path('classbasedcloth_api_with_view/', views.ClassBasedAPIViewClothAPI.as_view()),
    path('classbasedcloth_api_with_view/<int:pk>', views.ClassBasedAPIViewClothAPI.as_view()),
    path('venue_pdf', views.venue_pdf, name='venue_pdf')

]



# API Signature

# List/Create Shirts:

# Endpoint: /classbasedcloth_api_with_view/
# Method: GET (To list all shirts) and POST (To create a new shirt)

# Retrieve/Update/Delete Shirt:

# Endpoint: /classbasedcloth_api_with_view/<int:pk>/
# Method: GET (To retrieve a specific shirt),