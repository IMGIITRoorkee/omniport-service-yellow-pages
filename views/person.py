import swapper

from rest_framework import permissions, viewsets

from django.db.models import Q

from omniport.utils import switcher

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')

Person = swapper.load_model('kernel', 'Person')


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return the information on various people
    """

    permission_classes = [permissions.IsAuthenticated, ]

    serializer_class = AvatarSerializer
    pagination_class = None

    def get_queryset(self):
        """
        :return: ten person search objects
        """

        query = self.request.query_params.get('search', None)
        if query:
            person = Person.objects.filter(
                Q(short_name__icontains=query) |
                Q(full_name__icontains=query) |
                Q(user__username__icontains=query) |
                Q(student__enrolment_number__icontains=query) |
                Q(contact_information__primary_phone_number__icontains=query) |
                Q(contact_information__secondary_phone_number__icontains=query) |
                Q(contact_information__email_address__icontains=query) |
                Q(contact_information__institute_webmail_address__icontains=query)
            )
            return person[:10]
        return Person.objects.none()
