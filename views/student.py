import swapper

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from formula_one.enums.active_status import ActiveStatus

from omniport.utils import switcher

Student = swapper.load_model('kernel', 'Student')
StudentSerializer = switcher.load_serializer('kernel', 'Student')


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return the information on various people
    """

    permission_classes = [permissions.IsAuthenticated, ]

    serializer_class = StudentSerializer
    pagination_class = None

    def get_queryset(self):
        """
        :return: ten student search objects
        """

        query = self.request.query_params.get('search', None)
        if query:
            student = Student.objects_filter(ActiveStatus.IS_ACTIVE).filter(
                Q(enrolment_number__icontains=query) |
                Q(person__short_name__icontains=query) |
                Q(person__full_name__icontains=query) |
                Q(person__user__username__icontains=query) |
                Q(person__contact_information__primary_phone_number__icontains=query) |
                Q(person__contact_information__secondary_phone_number__icontains=query) |
                Q(person__contact_information__email_address__icontains=query) |
                Q(person__contact_information__institute_webmail_address__icontains=query)
            )
            return student[:10]
        return Student.objects.none()
