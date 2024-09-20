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
        for rep in self.reponse.all() : 
            affichage+= f"-{rep.texte}"
        return affichage
    
    @property
    def score(self):
        """Calculer le score de la question."""
        score = 0
        for reponse in self.reponse.all():
            if reponse.is_correct:
                score += reponse.question.note /reponse.question.number_of_correct_answers
            else :
                score -= reponse.question.note /reponse.question.number_of_correct_answers
        score = max(0,score)
        return affichage_score(score)
    
    @property
    def score_max(self):
        """Calculer le score max de la question."""
        return self.question.note
    

def is_int(x):
    '''Verifie si un nombre est un entier, car la fonction is_integer ne marche pas sur les entiers'''
    if(isinstance(x,int)):
        return True
    if x == int(x): 
        return True
    return False

def affichage_score(x):
    '''Affiche le score en entier ou en float à 2 chiffres après la virgule'''
    if(is_int(x)):
        return int(x)
    return round(x,2)