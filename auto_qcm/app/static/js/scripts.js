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

document.getElementById('theme-switch').addEventListener('change', function() {
    console.log('changed');
    if (this.checked) {
      document.body.classList.add('dark-mode');
      
      document.body.querySelector('.sidebar').classList.add('dark-mode');
      listItem=document.body.querySelectorAll('.nav-item');
      document.body.querySelector('.nav-item').classList.add('dark-mode');
      console.log("listitem",listItem);
      
      listItem.forEach(element => {
        element.classList.add('dark-mode');
      });


      
      var listButton = document.body.querySelector('.main-content').querySelectorAll('.button');
      listButton.forEach(element => {
        element.classList.add('dark-mode');
      });

      console.log(listButton);
      // document.body.querySelector('.navbar').classList.add('dark-mode');
      console.log('dark mode');
    } else {
      document.body.classList.remove('dark-mode');
      document.body.querySelector('.sidebar').classList.remove('dark-mode');
      document.body.querySelector('.main-content').querySelector('.button').classList.remove('dark-mode');
      test = document.body.querySelector('.main-content').querySelectorAll('.button');
      test.forEach(element => {
        element.classList.remove('dark-mode');
      });

      listItem=document.body.querySelectorAll('.nav-item');
      listItem.forEach(element => {
        element.classList.remove('dark-mode');
      }); 
      
    }
  });