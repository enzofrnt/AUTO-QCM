from django.db import models
from django.utils import timezone


class QCM(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField("Question", related_name="qcms", blank=True)
    date = models.DateTimeField(default=timezone.now)  # Définir une date par défaut
    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=1)  # 1 est l'ID d'un utilisateur par défaut
    

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "QCM"
        verbose_name_plural = "QCMs"

    def convertToXml(self):
        texte = '<?xml version="1.0"?><quiz>'
        for quest in self.questions.all():
            texte += quest.convertToXml()
        texte += "</quiz>"
        return texte
