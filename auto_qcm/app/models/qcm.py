from django.db import models


class QCM(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField("Question", related_name="qcms", blank=True)

    def __str__(self):
        return self.titre

    def convertToXml(self):

        return self.titre

    class Meta:
        verbose_name = "QCM"
        verbose_name_plural = "QCMs"
