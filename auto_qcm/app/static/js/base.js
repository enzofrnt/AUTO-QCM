document.addEventListener('DOMContentLoaded', function() {
    // Sélectionne tous les éléments de la barre de navigation avec la classe 'nav-item'
    var navItems = document.querySelectorAll('.nav-item');

    // Boucle sur chaque élément pour lui ajouter l'effet de hover
    navItems.forEach(function(item) {
      // Ajoute un effet lors du passage de la souris
      item.addEventListener('mouseover', function() {
        var theme = localStorage.getItem('theme') || 'light';
        if (theme === 'dark') {
            item.style.color = 'rgb(0, 0, 0)'; // Texte en noir

        } else {
            item.style.color = 'rgb(255, 255, 255)';
        }
      });

      // Enlève l'effet quand la souris quitte   l'élément
      item.addEventListener('mouseout', function() {
        item.style.color = ''; // Réinitialise la couleur du texte
      });
    });
});
