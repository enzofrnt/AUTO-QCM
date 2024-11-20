from logging import getLogger

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

logger = getLogger(__name__)


class Question(models.Model):
    nom = models.CharField(max_length=50)
    texte = models.CharField(max_length=255)
    note = models.IntegerField(default=1)
    melange_rep = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tag", related_name="questions", blank=True)
    creator = models.ForeignKey("Utilisateur", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True) 

    def __str__(self):
        return self.texte

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def get_correct_answers(self):
        """Retourne toutes les réponses correctes associées à cette question."""
        return self.reponses.filter(is_correct=True)

    @property
    def number_of_correct_answers(self):
        """Retourne le nombre de réponses correctes associées à cette question."""
        return self.get_correct_answers().count()

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
            + "<defaultgrade>"
            + str(self.note)
            + "</defaultgrade>"
            + "<single>"
            + ("false" if self.number_of_correct_answers > 1 else "true")
            + "</single>"
            + "<shuffleanswers>"
            + ("true" if self.melange_rep else "false")
            + "</shuffleanswers> "
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
            + "<defaultgrade>"
            + str(self.note)
            + "</defaultgrade>"
            + "<single>"
            + ("false" if self.number_of_correct_answers > 1 else "true")
            + "</single>"
            + "<shuffleanswers>"
            + ("true" if self.melange_rep else "false")
            + "</shuffleanswers> "
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
