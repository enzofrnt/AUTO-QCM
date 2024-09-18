from django.db import models

class ReponseQCM(models.Model):
    utilisateur = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reponses_qcm',default=1)
    qcm = models.ForeignKey('QCM', on_delete=models.CASCADE, related_name='reponses_qcm')
    reponses = models.ManyToManyField('ReponseQuestion')
    date_reponse = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Réponse QCM"
        verbose_name_plural = "Réponses QCM"
        unique_together = ('utilisateur', 'qcm', 'date_reponse')

    def __str__(self):
        return f"Reponse de {self.utilisateur.username} à {self.qcm.titre}"