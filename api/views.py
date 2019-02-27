from django.shortcuts import render
from events.models import Event
from rest_framework.generics import(
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from .serializers import (
    EventListSerializer,
    EventDetailSerializer,
    EventCreateUpdateSerializer,
    RegisterSerializer,
    BookingSerializer,
    Added_byListSerializer,
)    
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser,)
from rest_framework.filters import OrderingFilter, SearchFilter
from .permissions import IsUserAdd
import datetime

# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

class UpcomingEventListView(ListAPIView):
    current_date = datetime.datetime.today()  
    queryset = Event.objects.filter(datetime__gte=datetime.datetime.today(),)
    serializer_class = EventListSerializer
    permission_classes = [AllowAny,]
    filter_backends = [OrderingFilter, SearchFilter,]
    search_fields = ['title', 'description', 'datetime', 'added_by', 'seats']


class Added_byListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = Added_byListSerializer
    permission_classes = [AllowAny,]

    # def get_queryset()

class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [AllowAny,]

class EventCreateView(CreateAPIView):
    serializer_class = EventCreateUpdateSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user,)
    
class BookingView(CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        event_id= self.kwargs.get('event_id')
        event = Event.objects.get(id=event_id)
        serializer.save(user=self.request.user, event=event)

class EventUpdateView(RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsUserAdd,]


class EventDeleteView(DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsUserAdd,]



