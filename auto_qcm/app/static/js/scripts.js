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