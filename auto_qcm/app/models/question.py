from django.db import models
from django.core.exceptions import ValidationError


class Question(models.Model):
    nom = models.CharField(max_length=50)
    texte = models.CharField(max_length=255)
    tags = models.ManyToManyField("Tag", related_name="questions", blank=True)
    number_of_correct_answers = models.IntegerField(
        help_text="Nombre de bonnes réponses possibles. Doit être égal au nombre de réponses marquées comme correctes."
    )

    def __str__(self):
        return self.texte

    def convertToXml(self):
        # Convertir la question au format xml
        texte = (
            '<question type="multichoice">'
            + "<name>"
            + "<text>"  # Le vrai nom
            + self.nom
            + "</text>"
            + "</name>"
            + '<questiontext format="html"><text>'
            + '<![CDATA[<p dir="ltr" style="text-align: left;">'
            + self.texte
            + "<br></p>]]>"
            + "</text></questiontext>"
            + "<defaultgrade>1</defaultgrade>"
            + "<single>"
            + ("false" if self.number_of_correct_answers > 1 else "true")
            + "</single>"
            + "<shuffleanswers>true</shuffleanswers> "
            + "<answernumbering>abc</answernumbering>"
            + '<correctfeedback format="html">'
            + "<text>Votre réponse est correcte.</text>"
            + "</correctfeedback>"
            + '<partiallycorrectfeedback format="html">'
            + "<text>Votre réponse est partiellement correcte.</text>"
            + "</partiallycorrectfeedback>"
            + '<incorrectfeedback format="html">'
            + "<text>Votre réponse est incorrecte.</text>"
            + "</incorrectfeedback>"
        )

        for rep in self.reponses.all():
            texte += rep.convertToXml()

        texte += "</question>"

        return texte

    def convertToXmlSingle(self):
        """Convertit la question en xml pour télécharger directement"""
        texte = (
            '<?xml version="1.0"?><quiz>'
            + '<question type="multichoice">'
            + "<name>"
            + "<text>"
            + self.nom
            + "</text>"
            + "</name>"
            + '<questiontext format="html"><text>'
            + '<![CDATA[<p dir="ltr" style="text-align: left;">'
            + self.texte
            + "<br></p>]]>"
            + "</text></questiontext>"
            + "<defaultgrade>1</defaultgrade>"
            + "<single>"
            + ("false" if self.number_of_correct_answers > 1 else "true")
            + "</single>"
            + "<shuffleanswers>true</shuffleanswers> "
            + "<answernumbering>abc</answernumbering>"
            + '<correctfeedback format="html">'
            + "<text>Votre réponse est correcte.</text>"
            + "</correctfeedback>"
            + '<partiallycorrectfeedback format="html">'
            + "<text>Votre réponse est partiellement correcte.</text>"
            + "</partiallycorrectfeedback>"
            + '<incorrectfeedback format="html">'
            + "<text>Votre réponse est incorrecte.</text>"
            + "</incorrectfeedback>"
        )

        for rep in self.reponses.all():
            texte += rep.convertToXml()

        texte += "</question></quiz>"

        return texte

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
