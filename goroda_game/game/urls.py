from django.urls import path
from .views import CreateGameView, JoinGameView, MakeMoveView, SurrenderView, GameStateView

urlpatterns = [
    path('create/', CreateGameView.as_view(), name='create_game'),
    path('<int:game_id>/join/', JoinGameView.as_view(), name='join_game'),
    path('<int:game_id>/move/', MakeMoveView.as_view(), name='make_move'),
    path('<int:game_id>/surrender/', SurrenderView.as_view(), name='surrender'),
    path('<int:game_id>/state/', GameStateView.as_view(), name='game_state'),
]