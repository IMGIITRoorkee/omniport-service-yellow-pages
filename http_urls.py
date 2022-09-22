from django.urls import include, path
from rest_framework import routers

from yellow_pages.views.maintainer import MaintainerViewSet
from yellow_pages.views.person import PersonViewSet
from yellow_pages.views.student import StudentViewSet
from yellow_pages.views.filter import FilterViewSet

app_name = 'yellow_pages'

router = routers.SimpleRouter()
router.register('person', PersonViewSet, basename='person')
router.register('maintainer', MaintainerViewSet, basename='maintainer')
router.register('student', StudentViewSet, basename='student')
router.register('filter', FilterViewSet, basename='filter')

urlpatterns = [
    path('', include(router.urls)),
]
