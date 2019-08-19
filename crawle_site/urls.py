from django.urls import path,include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
urlpatterns = [
	path(r'', include(router.urls)),
	path(r'crawle/',views.CrawleView.as_view()),
]