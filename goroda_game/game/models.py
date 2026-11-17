from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    # Статусы игры
    STATUS_CHOICES = (
        ('waiting', 'Ожидание второго игрока'),
        ('active', 'В процессе'),
        ('finished', 'Завершена'),
    )
    
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player2', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    current_turn = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_turns')
    
    # Кто сдался (если игра завершена)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.id} - {self.player1.username} vs {self.player2.username if self.player2 else '...'}"


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves')
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Ходы всегда сортируются по времени

    def __str__(self):
        return f"{self.player.username}: {self.city}"