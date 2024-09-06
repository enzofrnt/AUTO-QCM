from django.db import models


class Reponse(models.Model):
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="reponses"
    )
    texte = models.CharField(max_length=255)
    is_correct = models.BooleanField(
        default=False, help_text="Cette réponse est-elle correcte ?"
    )

    def __str__(self):
        return self.texte

    class Meta:
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"

    def convertToXml(self):
        texteReponse = (
            '<answer fraction="'
            + (
                str(100 / self.question.reponses.filter(is_correct=True).count())
                if self.is_correct
                else "0"
            )
            + '" format="html">'
            + "<text>"
            + self.texte
            + "</text>"
            + '<feedback format="html">'
            + "<text/>"
            + "</feedback>"
            + "</answer>"
        )
        return texteReponse
