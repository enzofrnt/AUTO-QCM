from django.db import models


class ReponseQCM(models.Model):
    utilisateur = models.ForeignKey(
        "Utilisateur",
        on_delete=models.CASCADE,
        related_name="reponses_qcm",
        default=1,
    )
    qcm = models.ForeignKey(
        "QCM", on_delete=models.CASCADE, related_name="reponses_qcm"
    )
    reponses = models.ManyToManyField("ReponseQuestion")
    date_debut = models.DateTimeField()
    date_fin_reponse = models.DateTimeField()
    est_evalue = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Réponse QCM"
        verbose_name_plural = "Réponses QCM"
        unique_together = ("utilisateur", "qcm", "date_debut")

    def __str__(self):
        return f"Reponse de {self.utilisateur.username} à {self.qcm.titre}"

    @property
    def score(self):
        """Calculer le score du qcm."""
        score = 0
        for reponseQuestion in self.reponses.all():
            score += reponseQuestion.score
        return affichage_score(score)

    @property
    def score_max(self):
        """Calculer le score max du qcm."""
        score = 0
        for question in self.qcm.questions.all():
            score += question.note
        return score

    @property
    def duree(self):
        """Calculer la durée de réponse."""
        return self.date_fin_reponse - self.date_debut


def is_int(x):
    """Verifie si un nombre est un entier, car la fonction is_integer ne marche pas sur les entiers"""
    if isinstance(x, int):
        return True
    if x == int(x):
        return True
    return False


def affichage_score(x):
    """Affiche le score en entier ou en float à 2 chiffres après la virgule"""
    if is_int(x):
        return int(x)
    return round(x, 2)
