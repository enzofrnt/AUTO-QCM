$(document).ready(function () {
  const filterForm = $('#filterForm');
  const selectedTagsContainer = $('#selected-tags-container');

  // Fonction pour mettre à jour les tags sélectionnés et effectuer la requête AJAX
  function updateURLAndFetch() {
    const selectedTags = $('#tags .tag-badge.selected').map(function () {
      return $(this).data('tag-name');
    }).get();
    
    console.log('Tags sélectionnés:', selectedTags);  // Vérifiez les tags sélectionnés
    
    selectedTagsContainer.empty();
    selectedTags.forEach(function (tagName) {
      selectedTagsContainer.append(`<input type="hidden" name="tags" value="${tagName}">`);
    });

    fetchQuestions();
  }


  // Gérer la sélection des tags
 $(document).on('click', '#tags .tag-badge', function () {
    console.log('Tag cliqué', this);  // Vérifier si l'événement est bien capté
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
    console.log('Envoi des données pour la requête AJAX:', filterForm.serialize());  // Vérifier les données envoyées
    $.ajax({
      url: filterForm.attr('action') || window.location.href,
      type: 'GET',
      data: filterForm.serialize(),
      success: function(response) {
      console.log('Réponse du serveur:', response);  // Vérifiez la réponse du serveur
      $('#questions-list').html(response.html);
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
