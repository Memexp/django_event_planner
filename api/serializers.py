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
            'event',
        ]
    
    def validate(self, data):
        event_object = data.get('event')
        seats_left= int(data.get('tickets'))
        if event_object.seats_left() == 0:
            raise serializers.ValidationError("no seats avilable at theis time ") 
        elif seats_left > event_object.seats_left():
            raise serializers.ValidationError("you exceede the number of seats ")
        return data

class BookedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'tickets',
            'event',
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
    added_by = UserSerializer()
    class Meta:
        model = Event
        fields = '__all__'

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
        exclude = ["added_by", ]


            