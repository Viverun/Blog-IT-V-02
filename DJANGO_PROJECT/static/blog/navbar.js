/**
 * Navbar scroll behavior script
 * - Hides the navbar when scrolling down
 * - Shows the navbar when scrolling up
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get the navbar element
    const navbar = document.querySelector('.navbar');
    
    // Variables to track scroll position
    let lastScrollTop = 0;
    const scrollThreshold = 100; // Minimum scroll distance before hiding/showing navbar
    
    // Function to handle scroll events
    window.addEventListener('scroll', function() {
        // Get current scroll position
        const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Check if we've scrolled past the threshold
        if (currentScrollTop > scrollThreshold) {
            // Scrolling down
            if (currentScrollTop > lastScrollTop) {
                navbar.classList.add('navbar-hidden');
                navbar.classList.remove('navbar-visible');
            } 
            // Scrolling up
            else {
                navbar.classList.remove('navbar-hidden');
                navbar.classList.add('navbar-visible');
            }
        } else {
            // At the top of the page - always show navbar
            navbar.classList.remove('navbar-hidden');
            navbar.classList.add('navbar-visible');
        }
        
        // Update last scroll position
        lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;
    }, false);
});