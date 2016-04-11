from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from simple_app.restapi.model import Domain
from simple_app.restapi.serializer import DomainSerializer


class DomainView(APIView):

    def get(self, request, pk):
        instance = get_object_or_404(Domain, id=pk)
        if request.user.is_anonymous() and instance.is_private:
            raise NotAuthenticated

        serializer = DomainSerializer(instance)
        return Response(serializer.data)


class DomainsView(ListCreateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            self.queryset = Domain.objects.filter(is_private=False)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            raise NotAuthenticated
        return super().post(request, *args, **kwargs)
