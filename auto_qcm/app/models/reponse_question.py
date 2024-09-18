from django.db import models

class ReponseQuestion(models.Model):
    utilisateur = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='eleve',default=1)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question')
    reponse = models.ManyToManyField('Reponse', related_name='reponses')
    date = models.DateTimeField()

    class Meta:
        verbose_name = "Réponse Question"
        verbose_name_plural = "Réponses Questions"
        unique_together = ('utilisateur', 'question','date')

    def __str__(self):
        affichage = f"Réponse de {self.utilisateur.username} sur {self.question.nom} à {self.date} :"
        for rep in self.reponse : 
            affichage+= f"-{rep.texte}"
        return affichage