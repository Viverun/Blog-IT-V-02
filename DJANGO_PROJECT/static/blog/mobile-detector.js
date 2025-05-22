/**
 * Mobile Device Detector
 * Redirects mobile users to a "desktop only" page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Function to detect mobile devices
    function isMobileDevice() {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        
        // Check for mobile-specific patterns in user agent
        const mobileRegex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i;
        
        // Check screen width (typically mobile devices are under 768px wide)
        const isSmallScreen = window.innerWidth < 768;
        
        // Return true if either condition is met
        return mobileRegex.test(userAgent) || isSmallScreen;
    }
    
    // If we're on a mobile device and not already on the desktop-only page
    if (isMobileDevice() && !window.location.href.includes('/desktop-only/')) {
        // Save the current page URL to return to if accessed from desktop later
        const currentPage = window.location.href;
        localStorage.setItem('intendedDestination', currentPage);
        
        // Redirect to desktop-only page
        window.location.href = '/desktop-only/';
    }
});
