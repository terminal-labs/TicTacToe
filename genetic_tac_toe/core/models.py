from django.db import models


class MoveHash(models.Model):
    move_number = models.PositiveSmallIntegerField()  ## How many moves into the game are we?
    move_hash = models.CharField(max_length=40,unique=True, db_index=True)
    

class Moves(models.Model):
    move_1 = models.PositiveSmallIntegerField()
    move_2 = models.PositiveSmallIntegerField(null=True, blank=True)
    move_3 = models.PositiveSmallIntegerField(null=True, blank=True)
    move_4 = models.PositiveSmallIntegerField(null=True, blank=True)
    move_5 = models.PositiveSmallIntegerField(null=True, blank=True)
    move_6 = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    move_7 = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    move_8 = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    move_9 = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    x_won_game = models.BooleanField(default=False) ## This really means X won or forced a draw
    move_hash = models.ManyToManyField(MoveHash)

    @property
    def x_won(self):
        return bool(self.x_won_game)

    @property
    def game_finished(self):
        return bool(self.game_is_finished)


