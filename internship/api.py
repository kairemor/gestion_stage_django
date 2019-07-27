from rest_framework import permissions, viewsets, generics
from rest_framework.parsers import FileUploadParser

from internship.serializers import EnterpriseSerializers, ConventionSerializer
from rest_framework.response import Response

from .models import Enterprise, Convention
from django.db.models import Q

from accounts.models import Student


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all().order_by('-id')
    parser_class = (FileUploadParser,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnterpriseSerializers

    def get_queryset(self):
        queryset_search = Enterprise.objects.all().order_by('-id')
        query = self.request.GET.get('search')
        if query:
            queryset_search = queryset_search.filter(
                Q(name__icontains=query)
            ).distinct()
        return queryset_search
        

    def update(self, request, pk):

        enterprise = Enterprise.objects.get(id=pk)
        # when adding a list of student in a enterprise
        if 'students' in request.data:
            students_id = request.data['students']
            for student_id in students_id:
                student = Student.objects.get(id=student_id)
                student.enterprise = enterprise
                student.save()

        # When removing one student in a enterprise
        if 'student' in request.data:
            student = Student.objects.get(id=request.data['student'])
            student.enterprise = None
            student.save()

        if 'is_partner' in request.data:
            enterprise.is_partner = request.data['is_partner']

        enterprise.save()

        return Response(EnterpriseSerializers(enterprise).data)


class EnterpriseGET(generics.ListAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Enterprise.objects.all().order_by('-id')
    serializer_class = EnterpriseSerializers


class EnterprisePartnerView(generics.ListAPIView):
    queryset = Enterprise.objects.filter(is_partner=True).order_by('-id')
    serializer_class = EnterpriseSerializers


class EnterprisePotentialView(generics.ListAPIView):
    queryset = Enterprise.objects.filter(is_partner=False).order_by('-id')
    serializer_class = EnterpriseSerializers


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.all().order_by('-id')
    serializer_class = ConventionSerializer



    def create(self, request, *args, **kwargs):
        title = request.data['title']
        life_time = request.data['life_time']
        state = request.data['state']
        enterpriseId = request.data['enterprise']
        enterprise = Enterprise.objects.get(id=enterpriseId)
        convention = Convention(
            title=title, enterprise=enterprise, life_time=life_time, state=state)
        convention.save()
        return Response(ConventionSerializer(convention).data)

    def update(self, request, pk):
        convention = Convention.objects.get(id=pk)

        if 'life_time' in request.data:
            convention.life_time = request.data['life_time']
    
        convention.save()

        return Response(ConventionSerializer(convention).data)
