from django.db import models

class Question(models.Model):
    texte = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True)

    def __str__(self):
        return self.texte

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
