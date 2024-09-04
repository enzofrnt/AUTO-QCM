from django.db import models

class Reponse(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='reponses')
    texte = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', related_name='reponses', blank=True)

    def __str__(self):
        return self.texte

    class Meta:
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"