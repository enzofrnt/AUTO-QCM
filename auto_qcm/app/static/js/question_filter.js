$(document).ready(function () {
  const filterForm = $('#filterForm');
  const selectedTagsContainer = $('#selected-tags-container');

  // Variable pour stocker les IDs des questions sélectionnées
  let selectedQuestionIds = [];

  // Initialiser selectedQuestionIds au chargement de la page
  function initializeSelectedQuestions() {
    $('input[name="selected_questions"]:checked').each(function() {
      const questionId = $(this).val().toString();
      if (!selectedQuestionIds.includes(questionId)) {
        selectedQuestionIds.push(questionId);
      }
    });
    console.log('Selected Question IDs after initialization:', selectedQuestionIds);
  }

  // Appeler la fonction d'initialisation après que la page est complètement chargée
  initializeSelectedQuestions();

  // Fonction pour mettre à jour les tags sélectionnés et effectuer la requête AJAX
  function updateURLAndFetch() {
    const selectedTags = $('#tags .tag-badge.selected').map(function () {
      return $(this).data('tag-name');
    }).get();

    // Mettre à jour les champs cachés pour les tags
    selectedTagsContainer.empty();
    selectedTags.forEach(function (tagName) {
      selectedTagsContainer.append(`<input type="hidden" name="tags" value="${tagName}">`);
    });

    // Effectuer une requête AJAX pour récupérer les questions filtrées
    fetchQuestions();
  }

  // Gérer la sélection des tags
  $(document).on('click', '#tags .tag-badge', function () {
    $(this).toggleClass('selected');
    updateURLAndFetch();
  });

  // Fonction de debounce pour éviter les soumissions excessives
  function debounce(func, delay) {
    let debounceTimer;
    return function() {
      const context = this;
      const args = arguments;
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => func.apply(context, args), delay);
    }
  }

  // Appliquer le debounce à la saisie dans le champ de recherche
  filterForm.find('input[name="nom"]').on('input', debounce(function () {
    updateURLAndFetch();
  }, 500));

  // Fonction pour effectuer la requête AJAX et mettre à jour la liste des questions
  function fetchQuestions() {
    $.ajax({
      url: filterForm.attr('action') || window.location.href,
      type: 'GET',
      data: filterForm.serialize(),
      success: function(response) {
        // Remplacer le contenu de la liste des questions
        $('#questions-list').html(response.html);

        // Ré-attacher les événements
        reattachQuestionEvents();
      },
      error: function(xhr, status, error) {
        console.error('Erreur lors du chargement des questions:', error);
      }
    });
  }

  // Fonction pour ré-attacher les événements aux questions
  function reattachQuestionEvents() {
    // Gérer le clic sur les questions pour afficher/cacher les détails
    $('.question-row').off('click').on('click', function(e) {
      if (!$(e.target).is('input[type="checkbox"]') && !$(e.target).is('button') && !$(e.target).closest('button').length) {
        const questionId = $(this).data('question-id');
        $('#answers-' + questionId).slideToggle(300);
      }
    });

    // Gestion du survol pour afficher/masquer les boutons d'actions en utilisant visibility
    $('.question-container').off('mouseenter mouseleave').on('mouseenter', function() {
      var buttonList = $(this).find('.button-list');
      if (buttonList.length > 0) {
        buttonList.css('visibility', 'visible');
      }
    }).on('mouseleave', function() {
      var buttonList = $(this).find('.button-list');
      if (buttonList.length > 0) {
        buttonList.css('visibility', 'hidden');
      }
    });

    // Gérer les changements sur les cases à cocher
    $('input[name="selected_questions"]').off('change').on('change', function() {
      const questionId = $(this).val().toString();
      if ($(this).is(':checked')) {
        if (!selectedQuestionIds.includes(questionId)) {
          selectedQuestionIds.push(questionId);
        }
      } else {
        selectedQuestionIds = selectedQuestionIds.filter(id => id !== questionId);
      }
      console.log('Selected Question IDs after change:', selectedQuestionIds);
    });

    // Mettre à jour les cases à cocher en fonction de selectedQuestionIds
    $('input[name="selected_questions"]').each(function() {
      const questionId = $(this).val().toString();
      if (selectedQuestionIds.includes(questionId)) {
        $(this).prop('checked', true);
      } else {
        $(this).prop('checked', false);
      }
    });
  }

  // Initialiser les événements
  reattachQuestionEvents();

  // Avant la soumission du formulaire principal, ajouter des champs cachés pour les questions sélectionnées
  $('#qcmForm').on('submit', function() {
    // Supprimer les champs cachés existants pour éviter les doublons
    $('#selected-questions-container').remove();

    // Créer un conteneur pour les champs cachés
    const hiddenInputsContainer = $('<div id="selected-questions-container"></div>');

    // Ajouter un champ caché pour chaque question sélectionnée
    selectedQuestionIds.forEach(function(questionId) {
      hiddenInputsContainer.append(`<input type="hidden" name="selected_questions" value="${questionId}">`);
    });

    // Ajouter le conteneur au formulaire
    $(this).append(hiddenInputsContainer);

    console.log('Selected Question IDs before submission:', selectedQuestionIds);
  });
});