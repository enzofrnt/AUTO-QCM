$(document).ready(function () {
  const filterForm = $('#filterForm');
  const selectedTagsContainer = $('#selected-tags-container');

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

  // Fonction de debounce pour éviter les requêtes excessives
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
        if (typeof reattachQuestionEvents === 'function') {
          reattachQuestionEvents();
        }
      },
      error: function(xhr, status, error) {
        console.error('Erreur lors du chargement des questions:', error);
      }
    });
  }
});