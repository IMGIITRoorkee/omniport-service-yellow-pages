import swapper
from rest_framework import filters, permissions, viewsets

from omniport.utils import switcher

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')

Person = swapper.load_model('kernel', 'Person')


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return the information on various people
    """

    permission_classes = [permissions.IsAuthenticated, ]

    queryset = Person.objects.all()
    serializer_class = AvatarSerializer

    filter_backends = [filters.SearchFilter, ]
    search_fields = [
        # Self
        'short_name',
        'full_name',

        # User
        'user__username',

        # Student
        'student__enrolment_number',

        # Contact information
        'contact_information__primary_phone_number',
        'contact_information__secondary_phone_number',
        'contact_information__email_address',
        'contact_information__institute_webmail_address',
    ]

    pagination_class = None
