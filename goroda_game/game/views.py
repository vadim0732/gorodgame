from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Game, Move
from .serializers import GameSerializer, MoveSerializer
from django.shortcuts import render

class CreateGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Создаем игру, первый игрок - тот, кто отправил запрос
        game = Game.objects.create(player1=request.user, current_turn=request.user)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class JoinGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        
        if game.status != 'waiting':
            return Response({"error": "Игра уже начата или завершена"}, status=status.HTTP_400_BAD_REQUEST)
            
        if game.player1 == request.user:
            return Response({"error": "Вы не можете играть сами с собой"}, status=status.HTTP_400_BAD_REQUEST)

        game.player2 = request.user
        game.status = 'active'
        game.save()
        
        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)

class MakeMoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        
        # Базовые проверки
        if game.status != 'active':
            return Response({"error": "Игра не активна"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user != game.current_turn:
            return Response({"error": "Сейчас не ваш ход"}, status=status.HTTP_400_BAD_REQUEST)

        city_name = request.data.get('city', '').strip()
        if not city_name:
            return Response({"error": "Введите название города"}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем предыдущий ход, чтобы узнать последнюю букву
        last_move = game.moves.last()
        
        if last_move:
            last_city = last_move.city.lower()
            # Ищем последнюю букву, пропуская ъ, ы, ь
            last_letter = last_city[-1]
            if last_letter in ['ъ', 'ы', 'ь']:
                last_letter = last_city[-2]

            first_letter = city_name.lower()[0]
            
            if first_letter != last_letter:
                return Response({"error": f"Город должен начинаться на букву '{last_letter.upper()}'"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что такой город еще не называли (ищем без учета регистра)
        if game.moves.filter(city__iexact=city_name).exists():
            return Response({"error": "Этот город уже был назван"}, status=status.HTTP_400_BAD_REQUEST)

        # Все проверки пройдены, сохраняем ход
        with transaction.atomic():
            Move.objects.create(game=game, player=request.user, city=city_name)
            
            # Передаем ход другому игроку
            game.current_turn = game.player2 if request.user == game.player1 else game.player1
            game.save()

        return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)

class SurrenderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        
        if game.status != 'active':
            return Response({"error": "Игра не активна"}, status=status.HTTP_400_BAD_REQUEST)
            
        if request.user not in [game.player1, game.player2]:
            return Response({"error": "Вы не участвуете в этой игре"}, status=status.HTTP_403_FORBIDDEN)

        # Определяем победителя
        game.winner = game.player2 if request.user == game.player1 else game.player1
        game.status = 'finished'
        game.current_turn = None
        game.save()

        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)

class GameStateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        if request.user not in [game.player1, game.player2]:
            return Response({"error": "Вы не участник этой игры"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = GameSerializer(game)
        return Response(serializer.data)

def index_view(request):
    return render(request, 'game/index.html')