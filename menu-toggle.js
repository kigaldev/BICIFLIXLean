// Script para toggle del menú móvil

document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar los elementos necesarios
    const menuToggle = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.nav-menu');
    const userActions = document.querySelector('.user-actions');

    // Función para alternar las clases y manejar la apertura/cierre del menú
    function toggleMenu() {
        // Alternar la clase 'active' en el menú de navegación
        navMenu.classList.toggle('active');
        
        // Alternar la clase 'active' en las acciones de usuario
        userActions.classList.toggle('active');
        
        // Animación de transformación de las barras del menú hamburguesa
        menuToggle.classList.toggle('active');
    }

    // Añadir evento de clic al botón del menú
    menuToggle.addEventListener('click', toggleMenu);

    // Cerrar menú si se hace clic fuera de él
    document.addEventListener('click', function(event) {
        const isClickInsideMenu = menuToggle.contains(event.target) || 
                                  navMenu.contains(event.target) || 
                                  userActions.contains(event.target);
        
        if (!isClickInsideMenu) {
            navMenu.classList.remove('active');
            userActions.classList.remove('active');
            menuToggle.classList.remove('active');
        }
    });
});