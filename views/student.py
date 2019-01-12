import swapper
from rest_framework import filters, permissions, viewsets

from kernel.enums.active_status import ActiveStatus
from kernel.serializers.roles.student import StudentSerializer

Student = swapper.load_model('kernel', 'Student')


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return the information on various people
    """

    permission_classes = [permissions.IsAuthenticated, ]

    queryset = Student.objects_filter(ActiveStatus.IS_ACTIVE).all()
    serializer_class = StudentSerializer

    filter_backends = [filters.SearchFilter, ]
    search_fields = [
        # Self
        'enrolment_number',

        # Person
        'person__short_name',
        'person__full_name',

        # User
        'person__user__username',

        # Contact information
        'person__contact_information__primary_phone_number',
        'person__contact_information__secondary_phone_number',
        'person__contact_information__email_address',
        'person__contact_information__institute_webmail_address',
    ]

    pagination_class = None
