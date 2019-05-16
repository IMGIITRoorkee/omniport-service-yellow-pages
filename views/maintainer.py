import swapper
from rest_framework import filters, permissions, viewsets

from formula_one.enums.active_status import ActiveStatus
from omniport.utils import switcher

Maintainer = swapper.load_model('kernel', 'Maintainer')
MaintainerSerializer = switcher.load_serializer('kernel', 'Maintainer')


class MaintainerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return the information on various maintainers
    """

    permission_classes = [permissions.IsAuthenticated, ]

    queryset = Maintainer.objects_filter(ActiveStatus.IS_ACTIVE).all()
    serializer_class = MaintainerSerializer

    filter_backends = [filters.SearchFilter, ]
    search_fields = [
        # Self
        'role',
        'designation',
        'post',

        # Person
        'person__short_name',
        'person__full_name',

        # User
        'person__user__username',

        # Student
        'person__student__enrolment_number',

        # Contact information
        'person__contact_information__primary_phone_number',
        'person__contact_information__secondary_phone_number',
        'person__contact_information__email_address',
        'person__contact_information__institute_webmail_address',
    ]

    pagination_class = None
