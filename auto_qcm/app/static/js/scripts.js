$(document).ready(function() {

    // Initialisation du thème en fonction du sessionStorage
    function initializeTheme() {
        if (sessionStorage.getItem('theme') === 'dark') {
            applyDarkMode();
            $('#theme-switch').prop('checked', true); // Activer l'interrupteur du thème sombre
        } else {
            removeDarkMode();
            $('#theme-switch').prop('checked', false); // Désactiver l'interrupteur
        }
    }

    // Fonction pour appliquer le thème sombre
    function applyDarkMode() {
        $('body, .sidebar, .nav-item, .main-content .button-home').addClass('dark-mode');
    }

    // Fonction pour désactiver le thème sombre
    function removeDarkMode() {
        $('body, .sidebar, .nav-item, .main-content .button-home').removeClass('dark-mode');
    }

    // Toggle du thème sombre lors du changement du switch
    $('#theme-switch').on('change', function() {
        if ($(this).is(':checked')) {
            applyDarkMode();
            sessionStorage.setItem('theme', 'dark');
        } else {
            removeDarkMode();
            sessionStorage.setItem('theme', 'light'); // Ajout de l'état light dans le sessionStorage
        }
    });

    // Initialisation du thème lors du chargement de la page
    initializeTheme();

});
