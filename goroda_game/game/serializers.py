from rest_framework import serializers
from .models import Game, Move
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MoveSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)
    
    class Meta:
        model = Move
        fields = ['id', 'player', 'city', 'created_at']

class GameSerializer(serializers.ModelSerializer):
    player1 = UserSerializer(read_only=True)
    player2 = UserSerializer(read_only=True)
    current_turn = UserSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    moves = MoveSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'player1', 'player2', 'status', 'current_turn', 'winner', 'moves']