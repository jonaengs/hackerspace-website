import datetime

from django.db.models import Q
from django.http import QueryDict
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import DetailView, CreateView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from reservations.forms import ReservationForm
from reservations.models import Reservation, Queue
from reservations.serializers import ReservationSerializer


class QueueDetailView(DetailView):
    model = Queue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': ReservationForm(),
        })
        return context


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    @staticmethod
    def _parse_datetime_str(datetime_str):
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")

    def get_queryset(self):
        try:
            start = self._parse_datetime_str(self.request.GET['start'])
            end = self._parse_datetime_str(self.request.GET['end'])
            # Q() lets you combine queries
            queryset = Reservation.objects.filter(
                Q(parent_queue_id=self.kwargs['pk']) &
                Q(start__gte=start) &
                Q(end__lte=end)
            )
        except MultiValueDictKeyError:
            queryset = Reservation.objects.all()
        print(queryset)
        return queryset

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
