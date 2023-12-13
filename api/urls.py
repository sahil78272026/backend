from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('singer', views.SingerViewSet, basename='singer')
router.register('song', views.SongViewSet, basename='song')
router.register('movie', views.MovieViewSet, basename='movie')

urlpatterns = [
     # Function based View Practice
     path('stuinfo/<int:pk>', views.student_detail),
     path('stuinfo/', views.student_list),
     path('redis_recipe/', views.home_recipe),

     # Function based View Routers
     # path('stucreate/',views.student_create),

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
     path('venue_pdf', views.venue_pdf, name='venue_pdf'),
     path('generate-pdf', views.GenerateInvoice.as_view(), name='generate-pdf'),
     path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
     path('', include(router.urls)),
     path('select_rel/', views.select_rel),
     path('db_check/', views.db_check),
     path('multiple_json_object/', views.MultilplJsonObject.as_view()),
     path('addingData/', views.addingDataUsingFaker),
     path('getStudent/', views.getStudent),
     path('setcookie/', views.setcookie),
     path('showcookie/', views.showcookie),
     path('delete_co/', views.delete_co),


]
