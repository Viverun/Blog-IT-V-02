/**
 * Mobile Device Detector - DISABLED FOR TESTING
 * (Original functionality redirected mobile users to a "desktop only" page)
 */

document.addEventListener('DOMContentLoaded', function() {
    // Function is now disabled for testing
    console.log('Mobile detection disabled - allowing all devices to view content');
    
    // Store this value in case we need to restore the redirect later
    const currentPage = window.location.href;
    localStorage.setItem('intendedDestination', currentPage);
});
