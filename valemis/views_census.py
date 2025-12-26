"""
API Views for Census Survey
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import CensusSurvey, CensusMember, CensusQuestion
from .serializers_census import (
    CensusSurveySerializer,
    CensusSurveyListSerializer,
    CensusSurveyDetailSerializer,
    CensusMemberSerializer,
    CensusQuestionSerializer
)


class CensusSurveyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Census Survey CRUD operations
    """
    queryset = CensusSurvey.objects.all()
    serializer_class = CensusSurveySerializer

    def get_serializer_class(self):
        """Use different serializers for list vs detail"""
        if self.action == 'list':
            return CensusSurveyListSerializer
        elif self.action == 'retrieve':
            return CensusSurveyDetailSerializer
        return CensusSurveySerializer

    def get_queryset(self):
        """Filter surveys by query parameters"""
        queryset = CensusSurvey.objects.all()
        params = self.request.query_params

        # Filter by village
        village = params.get('village')
        if village:
            queryset = queryset.filter(village__icontains=village)

        # Filter by enumerator
        enumerator = params.get('enumerator')
        if enumerator:
            queryset = queryset.filter(q1_kode_enumerator__icontains=enumerator)

        # Filter by district
        district = params.get('district')
        if district:
            queryset = queryset.filter(district__icontains=district)

        # Filter by date range
        date_from = params.get('date_from')
        date_to = params.get('date_to')
        if date_from:
            queryset = queryset.filter(survey_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(survey_date__lte=date_to)

        return queryset

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get survey statistics
        /api/valemis/census/statistics/
        """
        total_surveys = CensusSurvey.objects.count()
        total_villages = CensusSurvey.objects.values('village').distinct().count()

        # Gender distribution
        gender_dist = {}
        for choice in ['Laki-laki', 'Perempuan']:
            count = CensusSurvey.objects.filter(q10_jenis_kelamin=choice).count()
            gender_dist[choice] = count

        # Religion distribution
        religion_dist = {}
        for survey in CensusSurvey.objects.filter(q5_agama__isnull=False):
            religion = survey.q5_agama or 'Tidak diisi'
            religion_dist[religion] = religion_dist.get(religion, 0) + 1

        # Employment status
        employment_dist = {}
        for survey in CensusSurvey.objects.filter(q19_bekerja_12_bulan__isnull=False):
            status = survey.q19_bekerja_12_bulan or 'Tidak diisi'
            employment_dist[status] = employment_dist.get(status, 0) + 1

        return Response({
            'total_surveys': total_surveys,
            'total_villages': total_villages,
            'gender_distribution': gender_dist,
            'religion_distribution': religion_dist,
            'employment_distribution': employment_dist,
        })

    @action(detail=False, methods=['get'])
    def by_village(self, request):
        """
        Get surveys grouped by village
        /api/valemis/census/by_village/
        """
        villages = CensusSurvey.objects.values('village').annotate(
            count=Count('id')
        ).order_by('-count')

        data = []
        for village in villages:
            village_name = village['village'] or 'Tidak diketahui'
            data.append({
                'village': village_name,
                'count': village['count']
            })

        return Response(data)

    @action(detail=True, methods=['get', 'post', 'put'])
    def members(self, request, pk=None):
        """
        Manage household members
        GET /api/valemis/census/{id}/members/ - List members
        POST /api/valemis/census/{id}/members/ - Add member
        """
        survey = self.get_object()

        if request.method == 'GET':
            members = survey.members.all()
            serializer = CensusMemberSerializer(members, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CensusMemberSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(household=survey)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CensusMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Census Member CRUD operations
    """
    queryset = CensusMember.objects.all()
    serializer_class = CensusMemberSerializer

    def get_queryset(self):
        """Filter members by household if provided"""
        queryset = CensusMember.objects.all()
        household_id = self.request.query_params.get('household')
        if household_id:
            queryset = queryset.filter(household_id=household_id)
        return queryset


class CensusQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Census Questions (read-only)
    Used to populate dropdown options in forms
    """
    queryset = CensusQuestion.objects.all()
    serializer_class = CensusQuestionSerializer

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get questions grouped by category
        /api/valemis/questions/by_category/
        """
        category = request.query_params.get('category')

        if category:
            questions = CensusQuestion.objects.filter(category=category)
        else:
            questions = CensusQuestion.objects.all()

        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)
