from django.db import models

class ReponseQuestion(models.Model):
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='eleve')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question')
    reponse = models.ManyToManyField('Reponse', related_name='reponses')
    date = models.DateTimeField()

    class Meta:
        verbose_name = "Réponse Question"
        verbose_name_plural = "Réponses Questions"
        unique_together = ('eleve', 'question','date')

    def __str__(self):
        return f"Réponse de {self.eleve.name} à {self.question} à {self.date}"