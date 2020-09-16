from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime
from .models import Flight, Booking, Profile


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['destination', 'time', 'price', 'id']


class BookingSerializer(serializers.ModelSerializer):
    flight=serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
     )
 #Show the destination instead of the flight id using SlugRelatedField.
    class Meta:
        model = Booking
        fields = ['flight', 'date', 'id' ,'title']


class BookingDetailsSerializer(serializers.ModelSerializer):

    total=serializers.SerializerMethodField()# which is the total cost of the flight for all passengers.
    flight=FlightSerializer() # Use the FlightSerializer to display the flight info.

    class Meta:
        model = Booking
        fields = ['flight', 'date', 'passengers', 'id' ,'total']

    def get_total(self, obj):
       return obj.passengers* obj.flight.price


class AdminUpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['date', 'passengers']


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['passengers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
     user = UserSerializer()
     past_bookings=serializers.SerializerMethodField()

     tier=serializers.SerializerMethodField()
     class Meta:
        model = Profile
        fields = ['user', 'miles' ,'past_bookings' , 'tier']

     def get_past_bookings(self,obj):
         bookings = Booking.objects.filter(user=obj.user,date__lt=datetime.today())
         #past_bookings= BookingSerializer(bookings)
         serializer = BookingSerializer(instance=bookings,many=True)

         return serializer.data


     def get_tier( self, obj):
        tier=obj.miles
        if 0 <= tier <=9999:
            return "Blue"
        elif 10000 <= tier <= 59999:
            return " Silver"
        elif 60000 <= tier <= 99999:
            return " Gold"
        elif tier >=100000 :
            return "Platinum"
