import swapper

from distutils.util import strtobool

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Q

from omniport.utils import switcher

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')

Person = swapper.load_model('kernel', 'Person')
Branch = swapper.load_model('Kernel', 'Branch')
Degree = swapper.load_model('Kernel', 'Degree')

class FilterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return the information on various people
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AvatarSerializer
    pagination_class = None

    def get_queryset(self):
        """
        :return: person objects for applied filters
        """

        params = self.request.GET
        queryset = Person.objects.all()
        queryset = self.apply_filters(self.request, queryset)
        return queryset

    def apply_filters(self, request, queryset):
        """
        Return a dict with all the filters populated with the
        filters received from query params.
        """
        filters = {}
        params = self.request.GET

        """
        Filter based on Year
        """
        year = params.get('year', None)
        
        if year:
            year_array = year.split(',')
            filters['student__current_year__in'] = year_array

        """
        Filter based on Branch
        """
        branch = params.get('branch', None)

        if branch:
            branch_array = branch.split(',')
            filters['student__branch__code__in'] = branch_array

        """
        Filter based on Degree
        """
        degree = params.get('degree', None)
        if degree:
            degree_array = degree.split(',')
            filters['student__branch__degree__code__in'] = degree_array

        """
        Filter based on Branch and Degree and Year
        """
        queryset_by = Person.objects.none()
        by = params.get('by', None)
        
        if by:
            by_array = by.split(',')
            for by_obj in by_array:
                by_obj = by_obj.split('.')
                by_year = by_obj[0]
                by_branch = by_obj[1]
                by_people = Person.objects.filter(
                    Q(student__isnull=False)&
                    Q(student__current_year=by_year)&
                    Q(student__branch__code=by_branch))
                queryset_by |= (queryset&by_people)

        """
        Filter students
        """
        is_student = params.get('is_student', None)
        if is_student:
            is_student = strtobool(is_student)
            if is_student:
                queryset = queryset.filter(student__isnull=False)
            else:
                queryset = queryset.filter(student__isnull=True)

        if filters=={}:
            queryset = Person.objects.none()

        queryset = queryset.filter(**filters)
        queryset |= queryset_by
        queryset = queryset.order_by('-datetime_modified')

        return queryset

    @action(detail=False, methods=['get'])
    def get_data(self, request):
        response = {}

        branches = Branch.objects.all()
        response['branches'] = {
            branch.code : branch.name for branch in branches
        }

        degrees = Degree.objects.all()
        response['degrees'] = {
            degree.code : degree.name for degree in degrees
        }

        return Response(response)