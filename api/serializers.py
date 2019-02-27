from rest_framework import serializers
from events.models import Event, Booking
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'added_by',]


class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = [
            'tickets',
        ]

class EventListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    
    

    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'datetime',
            'added_by',
            'detail',
            'update',
            'delete',
            ]
class Added_byListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    added_by = UserSerializer()
    events = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'datetime',
            'added_by',
            'detail',
            'update',
            'delete',
            'events',
            ]
    def get_events(self, obj):
        events = Event.objects.all(event=obj)
        event_list = EventSerializer(events, many=True).data
        print(event_list)
        return event_list

class EventDetailSerializer(serializers.ModelSerializer):
    attends = Added_byListSerializer(many=True)
    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    Book = serializers.HyperlinkedIdentityField(
        view_name = "api-book",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )    
    added_by = UserSerializer()

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'added_by',
            'description',
            'location',
            'datetime',
            'seats',
            'update',
            'delete',
            'Book',
            'attends',
            ]
            
    
        

class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'datetime',
            'added_by',
            'seats',
            ]