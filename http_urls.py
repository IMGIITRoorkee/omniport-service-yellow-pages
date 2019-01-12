from django.urls import include, path
from rest_framework import routers

from yellow_pages.views.maintainer import MaintainerViewSet
from yellow_pages.views.person import PersonViewSet
from yellow_pages.views.student import StudentViewSet

app_name = 'yellow_pages'

router = routers.SimpleRouter()
router.register('person', PersonViewSet, base_name='person')
router.register('maintainer', MaintainerViewSet, base_name='maintainer')
router.register('student', StudentViewSet, base_name='student')

urlpatterns = [
    path('', include(router.urls)),
]
