// JavaScript to hide link previews when hovering
document.addEventListener('DOMContentLoaded', function() {
    // Get all links in the document
    const links = document.querySelectorAll('a');
    
    // For each link
    links.forEach(link => {
        // Store the original href
        const originalHref = link.getAttribute('href');
        
        // Remove any title attribute that might show on hover
        if (link.hasAttribute('title')) {
            link.removeAttribute('title');
        }
        
        // Prevent the browser from showing the URL in the status bar
        link.addEventListener('mouseover', function(e) {
            // This prevents the default behavior which includes showing the URL
            window.status = '';
            return true;
        });
        
        // Ensure the link still works correctly
        link.addEventListener('click', function(e) {
            if (originalHref) {
                if (originalHref.startsWith('#')) {
                    // For anchor links, let the default behavior work
                    return true;
                } else {
                    // For regular links, navigate programmatically
                    window.location.href = originalHref;
                    e.preventDefault();
                }
            }
        });
    });
});