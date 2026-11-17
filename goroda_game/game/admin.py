from django.contrib import admin
from .models import Game, Move

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'status', 'current_turn', 'winner')

@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'player', 'city', 'created_at')