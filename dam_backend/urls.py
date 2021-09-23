from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from main import views


router = routers.DefaultRouter()
router.register(r'msections', views.MsectionViewSet)
router.register(r'mpoints', views.MpointViewSet)
router.register(r'mvalues', views.MvalueViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]