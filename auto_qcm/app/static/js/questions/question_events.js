$(document).ready(function () {
    // Variable globale pour stocker les IDs des questions sélectionnées
    window.selectedQuestionIds = [];

    $('.delete-question-btn').off('click').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation(); // Empêche le clic de se propager à l'élément parent
        const questionId = $(this).data('question-id');
        if (confirm('Voulez-vous vraiment supprimer cette question ?')) {
            window.location.href = deleteUrlTemplate.replace('0', questionId);
        }
    });
      
    // Répétez pour les autres boutons
    $('.edit-question-btn').off('click').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    const questionId = $(this).data('question-id');
    window.location.href = editUrlTemplate.replace('0', questionId);
    });
      
    $('.export-question-btn').off('click').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    const questionId = $(this).data('question-id');
    window.location.href = exportUrlTemplate.replace('0', questionId);
    });
  
    // Initialiser selectedQuestionIds au chargement de la page
    function initializeSelectedQuestions() {
      $('input[name="selected_questions"]:checked').each(function() {
        const questionId = $(this).val().toString();
        if (!window.selectedQuestionIds.includes(questionId)) {
          window.selectedQuestionIds.push(questionId);
        }
      });
    }
  
    // Appeler la fonction d'initialisation après que la page est complètement chargée
    initializeSelectedQuestions();
  
    // Fonction pour ré-attacher les événements aux questions
    window.reattachQuestionEvents = function() {
      // Gérer le clic sur les questions pour afficher/cacher les détails
      $('.question-row').off('click').on('click', function(e) {
        if (!$(e.target).is('input[type="checkbox"]') && !$(e.target).is('button') && !$(e.target).closest('button').length) {
          const questionId = $(this).data('question-id');
          $('#answers-' + questionId).slideToggle(300);
        }
      });
  
      // Gestion du survol pour afficher/masquer les boutons d'actions
      $('.question-container').off('mouseenter mouseleave').on('mouseenter', function() {
        const buttonList = $(this).find('.button-list');
        if (buttonList.length > 0) {
          buttonList.css('visibility', 'visible');
        }
      }).on('mouseleave', function() {
        const buttonList = $(this).find('.button-list');
        if (buttonList.length > 0) {
          buttonList.css('visibility', 'hidden');
        }
      });
  
      // Gérer les changements sur les cases à cocher
      $('input[name="selected_questions"]').off('change').on('change', function() {
        const questionId = $(this).val().toString();
        if ($(this).is(':checked')) {
          if (!window.selectedQuestionIds.includes(questionId)) {
            window.selectedQuestionIds.push(questionId);
          }
        } else {
          window.selectedQuestionIds = window.selectedQuestionIds.filter(id => id !== questionId);
        }
      });
  
      // Mettre à jour les cases à cocher en fonction de selectedQuestionIds
      $('input[name="selected_questions"]').each(function() {
        const questionId = $(this).val().toString();
        if (window.selectedQuestionIds.includes(questionId)) {
          $(this).prop('checked', true);
        } else {
          $(this).prop('checked', false);
        }
      });
    };
  
    // Initialiser les événements
    reattachQuestionEvents();
  
    // Avant la soumission du formulaire principal, ajouter des champs cachés pour les questions sélectionnées
    $('#qcmForm').on('submit', function() {
      // Supprimer les champs cachés existants pour éviter les doublons
      $('#selected-questions-container').remove();
  
      // Créer un conteneur pour les champs cachés
      const hiddenInputsContainer = $('<div id="selected-questions-container"></div>');
  
      // Ajouter un champ caché pour chaque question sélectionnée
      window.selectedQuestionIds.forEach(function(questionId) {
        hiddenInputsContainer.append(`<input type="hidden" name="selected_questions" value="${questionId}">`);
      });
  
      // Ajouter le conteneur au formulaire
      $(this).append(hiddenInputsContainer);
      });
  });