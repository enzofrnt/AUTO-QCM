$(document).ready(function() {

    // Fonction pour appliquer le thème sombre
    function applyDarkMode() {
        $('html').addClass('dark-mode');
    }

    // Fonction pour désactiver le thème sombre
    function removeDarkMode() {
        $('html').removeClass('dark-mode');
    }

    // Toggle du thème sombre lors du changement du switch
    $('#theme-switch').on('change', function() {
        if ($(this).is(':checked')) {
            applyDarkMode();
            localStorage.setItem('theme', 'dark');
        } else {
            removeDarkMode();
            localStorage.setItem('theme', 'light');
        }
    });

    // Initialisation du thème lors du chargement de la page
    var theme = localStorage.getItem('theme') || 'light'; // Par défaut 'light'
    if (theme === 'dark') {
        applyDarkMode();
        $('#theme-switch').prop('checked', true);
    } else {
        removeDarkMode();
        $('#theme-switch').prop('checked', false);
    }
});
