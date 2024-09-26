// static/js/question_filter.js
$(document).ready(function () {
  const filterForm = $('#filterForm');
  const selectedTagsContainer = $('#selected-tags-container');

  // Variable pour stocker les IDs des questions sélectionnées
  let selectedQuestionIds = [];

  // URL templates pour les actions (définis dans le template)
  var deleteUrlTemplate = window.deleteUrlTemplate || '';
  var exportUrlTemplate = window.exportUrlTemplate || '';
  var editUrlTemplate = window.editUrlTemplate || '';

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

  // Intercepter la soumission du formulaire pour éviter le rechargement complet
  filterForm.on('submit', function(e) {
    e.preventDefault();
    fetchQuestions();
  });

  // Fonction pour effectuer la requête AJAX et mettre à jour la liste des questions
  function fetchQuestions() {
    // Stocker les IDs des questions sélectionnées
    selectedQuestionIds = $('input[name="selected_questions"]:checked').map(function() {
      return $(this).val();
    }).get();

    $.ajax({
      url: filterForm.attr('action') || window.location.href,
      type: 'GET',
      data: filterForm.serialize(),
      success: function(response) {
        // Remplacer le contenu de la liste des questions
        $('#questions-list').html(response.html);

        // Réattacher les événements
        reattachQuestionEvents();

        // Restaurer les cases à cocher sélectionnées
        $('input[name="selected_questions"]').each(function() {
          if (selectedQuestionIds.includes($(this).val())) {
            $(this).prop('checked', true);
          }
        });
      },
      error: function(xhr, status, error) {
        console.error('Erreur lors du chargement des questions:', error);
      }
    });
  }

  // Fonction pour réattacher les événements aux questions
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
  
    // Attacher les événements de clic sur les boutons seulement si les boutons existent
    if ($('.delete-question-btn').length > 0) {
      $('.delete-question-btn').off('click').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const questionId = $(this).data('question-id');
        if (confirm('Voulez-vous vraiment supprimer cette question ?')) {
          window.location.href = deleteUrlTemplate.replace('0', questionId);
        }
      });
    }
  
    if ($('.export-question-btn').length > 0) {
      $('.export-question-btn').off('click').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const questionId = $(this).data('question-id');
        window.location.href = exportUrlTemplate.replace('0', questionId);
      });
    }
  
    if ($('.edit-question-btn').length > 0) {
      $('.edit-question-btn').off('click').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const questionId = $(this).data('question-id');
        window.location.href = editUrlTemplate.replace('0', questionId);
      });
    }
  
    // Gérer les changements sur les cases à cocher
    $('input[name="selected_questions"]').off('change').on('change', function() {
      updateSelectedQuestions();
    });
  }

  // Fonction pour mettre à jour la liste des questions sélectionnées
  function updateSelectedQuestions() {
    selectedQuestionIds = $('input[name="selected_questions"]:checked').map(function() {
      return $(this).val();
    }).get();
  }

  // Initialiser les événements
  reattachQuestionEvents();
});