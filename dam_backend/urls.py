from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from main import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.FileUploadView.as_view()),
    path('admin/', admin.site.urls),
]