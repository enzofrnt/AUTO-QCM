from django.db import models
from django.core.exceptions import ValidationError


class Question(models.Model):
    texte = models.CharField(max_length=255)
    tags = models.ManyToManyField("Tag", related_name="questions", blank=True)
    number_of_correct_answers = models.IntegerField(
        help_text="Nombre de bonnes réponses possibles. Doit être égal au nombre de réponses marquées comme correctes."
    )

    def __str__(self):
        return self.texte

    def convertToXml(self):
        # Convertir la question au format xml
        return self.texte

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def clean(self):
        """Validation personnalisée pour vérifier le nombre de bonnes réponses."""
        correct_answers_count = self.reponses.filter(is_correct=True).count()

        if correct_answers_count != self.number_of_correct_answers:
            raise ValidationError(
                f"La question doit avoir exactement {self.number_of_correct_answers} bonne(s) réponse(s), "
                f"mais elle en a {correct_answers_count}."
            )

        # Verify thta we have more response than the number of expected correct answers + 1
        if self.reponses.count() < self.number_of_correct_answers + 1:
            raise ValidationError(
                "La question doit avoir un nombre total de réponse supérieur au nombre de bonne réponse + 1."
            )

    def get_correct_answers(self):
        """Retourne toutes les réponses correctes associées à cette question."""
        return self.reponses.filter(is_correct=True)
