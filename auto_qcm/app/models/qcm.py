from django.db import models
from django.utils import timezone


class QCM(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField("Question", related_name="qcms", blank=True)
    date_modif = (
        models.DateTimeField()
    )  # Apparement le auto_add c'est pas génial --> Me met pleins d'erreurs
    creator = models.ForeignKey(
        "Utilisateur", on_delete=models.CASCADE
    )  # 1 est l'ID d'un utilisateur par défaut
    est_accessible = models.BooleanField(default=False)
    nb_reponses = models.IntegerField(default=1)

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        """Quand on sauvegarde on met a jour la date de modification"""
        self.date_modif = timezone.now()
        return super(QCM, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "QCM"
        verbose_name_plural = "QCMs"

    @property
    def number_of_questions(self):
        """Retourne le nombre de questions associées à ce qcm."""
        return self.questions.count()

    def convertToXml(self):
        texte = '<?xml version="1.0"?><quiz>'
        for quest in self.questions.all():
            texte += quest.convertToXml()
        texte += "</quiz>"
        return texte

    def convert_to_latex(self):
        """
        Convertit un QCM en document LaTeX.
        """
        # Début du document LaTeX
        latex_content = r"""\documentclass{article}

    \usepackage[latin1]{inputenc}
    \usepackage[T1]{fontenc}

    \usepackage[bloc,completemulti]{automultiplechoice}
    \usepackage{multicol}
    \begin{document}

    \AMCrandomseed{1237893}

    \element{amc}{
    """

        # Boucle à travers les questions associées au QCM
        for question in self.questions.all():
            # Déterminer le type de question
            question_type = (
                "questionmult"
                if question.reponses.filter(is_correct=True).count() > 1
                else "question"
            )

            # Ajouter la question LaTeX
            latex_content += f"  \\begin{{{question_type}}}{{{question.nom}}}\n"
            latex_content += "    \\bareme{b=2}\n"  # Ajustez le barème si nécessaire
            latex_content += f"    {question.texte}\n"
            latex_content += "    \\begin{multicols}{2}\n"
            latex_content += "      \\begin{reponses}\n"

            # Boucle à travers les réponses associées à la question
            for reponse in question.reponses.all():
                if reponse.is_correct:
                    latex_content += f"        \\bonne{{{reponse.texte}}}\n"
                else:
                    latex_content += f"        \\mauvaise{{{reponse.texte}}}\n"

            latex_content += "      \\end{reponses}\n"
            latex_content += "    \\end{multicols}\n"
            latex_content += f"  \\end{{{question_type}}}\n"

        # Fermer l'environnement \element{amc}
        latex_content += "}\n"

        # Ajouter l'exemplaire (entête et corps du document)
        latex_content += r"""
    \exemplaire{10}{

    %%% début de l'en-tête des copies :

    \noindent{\bf Classe d'application d'AMC  \hfill Examen du 01/01/2010}

    \vspace{2ex}

    Cet examen a pour but d'illustrer l'utilisation d'\emph{Auto Multiple Choice}. Vous pourrez trouver sur le site d'AMC les copies de Jojo Boulix et André Roullot afin de tester la saisie automatique, ainsi que le fichier listant les étudiants de la classe d'application d'AMC (dont font partie Jojo et André) afin de tester l'association automatique à partir des numéros d'étudiants.

    \vspace{3ex}

    \noindent\AMCcode{etu}{8}\hspace*{\fill}
    \begin{minipage}{.5\linewidth}
    $\longleftarrow{}$ codez votre numéro d'étudiant ci-contre, et écrivez votre nom et prénom ci-dessous.

    \vspace{3ex}

    \champnom{\fbox{
        \begin{minipage}{.9\linewidth}
        Nom et prénom :

        \vspace*{.5cm}\dotfill
        \vspace*{1mm}
        \end{minipage}
    }}\end{minipage}

    \vspace{1ex}

    \noindent\hrulefill

    \vspace{2ex}

    \begin{center}
    Les questions faisant apparaître le symbole \multiSymbole{} peuvent présenter zéro, une ou plusieurs bonnes réponses. Les autres ont une unique bonne réponse.
    \end{center}

    \noindent\hrulefill

    \vspace{2ex}
    %%% fin de l'en-tête

    \melangegroupe{amc}
    \restituegroupe{amc}

    \clearpage

    }

    \end{document}
    """

        return latex_content
