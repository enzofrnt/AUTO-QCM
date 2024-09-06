from django.db import models
from django.core.exceptions import ValidationError
from logging import getLogger
from django.db.models.signals import pre_save
from django.dispatch import receiver

logger = getLogger(__name__)

class Question(models.Model):
    texte = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True)

    def __str__(self):
        return self.texte

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"        

    def get_correct_answers(self):
        """Retourne toutes les réponses correctes associées à cette question."""
        return self.reponses.filter(is_correct=True)
    
    @property
    def number_of_correct_answers(self):
        """Retourne le nombre de réponses correctes associées à cette question."""
        return self.get_correct_answers().count()
