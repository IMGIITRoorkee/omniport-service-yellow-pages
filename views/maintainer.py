import swapper
from rest_framework import filters, permissions, viewsets

from django.db.models import Q

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

    pagination_class = None

    def get_queryset(self):
        """
        :return: 10 maintainer search objects
        """

        query = self.request.query_params.get('search', None)
        maintainer = Maintainer.objects_filter(ActiveStatus.IS_ACTIVE).filter(
            Q(role__icontains=query) |
            Q(designation__icontains=query) |
            Q(post__icontains=query) |
            Q(person__short_name__icontains=query) |
            Q(person__full_name__icontains=query) |
            Q(person__user__username__icontains=query) |
            Q(person__student__enrolment_number__icontains=query) |
            Q(person__contact_information__primary_phone_number__icontains=query) |
            Q(person__contact_information__secondary_phone_number__icontains=query) |
            Q(person__contact_information__email_address__icontains=query) |
            Q(person__contact_information__institute_webmail_address__icontains=query)
        )
        return maintainer[:10]
