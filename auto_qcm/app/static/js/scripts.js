function toggleSidebar() {
    
    document.querySelector('.sidebar').classList.toggle('collapsed');
    document.querySelector('.toggle-btn').classList.toggle('collapsed');
    
    const icon = document.querySelector('.toggle-btn i');

    if (icon.classList.contains('bi-caret-left')) {
        icon.classList.remove('bi-caret-left');
        icon.classList.add('bi-caret-right');
    } else {
        icon.classList.remove('bi-caret-right');
        icon.classList.add('bi-caret-left');
    }
    
    console.log('toggled');
}

if (sessionStorage.getItem('theme') === 'dark') {
  document.body.classList.add('dark-mode');
  document.body.querySelector('.sidebar').classList.add('dark-mode');
  document.body.querySelectorAll('.nav-item').forEach(element => {
      element.classList.add('dark-mode');
  });
  document.body.querySelector('.main-content').querySelectorAll('.button-home').forEach(element => {
      element.classList.add('dark-mode');
  });

  document.getElementById('theme-switch').checked = true; // Assurez-vous que le bouton de basculement est en mode "activé"
}

document.getElementById('theme-switch').addEventListener('change', function() {
  if (this.checked) {
      // Applique le thème sombre
      document.body.classList.add('dark-mode');
      document.body.querySelector('.sidebar').classList.add('dark-mode');
      document.body.querySelectorAll('.nav-item').forEach(element => {
          element.classList.add('dark-mode');
      });
      
      document.body.querySelector('.main-content').querySelectorAll('.button-home').forEach(element => {
          element.classList.add('dark-mode');
      });

      console.log('dark mode');
      sessionStorage.setItem('theme', 'dark');
  } else {
      // Retire le thème sombre
      document.body.classList.remove('dark-mode');
      document.body.querySelector('.sidebar').classList.remove('dark-mode');
      document.body.querySelectorAll('.nav-item').forEach(element => {
          element.classList.remove('dark-mode');
      });
      document.body.querySelector('.main-content').querySelectorAll('.button-home').forEach(element => {
          element.classList.remove('dark-mode');
      });

      // Retire le thème du sessionStorage
      console.log('light mode');
      sessionStorage.removeItem('theme');
  }
});