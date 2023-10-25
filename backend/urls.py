#Import from DRF


# import from django
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# Local Import
from api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('api/', include('api.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# API Signature

# List/Create Shirts:

# Endpoint: /classbasedcloth_api_with_view/
# Method: GET (To list all shirts) and POST (To create a new shirt)

# Retrieve/Update/Delete Shirt:

# Endpoint: /classbasedcloth_api_with_view/<int:pk>/
# Method: GET (To retrieve a specific shirt),