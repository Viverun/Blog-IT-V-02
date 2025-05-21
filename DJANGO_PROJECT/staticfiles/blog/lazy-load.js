// Lazy loading of images for better mobile performance
document.addEventListener('DOMContentLoaded', function() {
    // Check if the browser supports IntersectionObserver
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                // If the image is in the viewport
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Replace the src with the data-src
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                    }
                    
                    // Replace srcset if available
                    if (img.dataset.srcset) {
                        img.srcset = img.dataset.srcset;
                    }
                    
                    // Once loaded, stop watching this element
                    observer.unobserve(img);
                }
            });
        }, {
            // Options: only load when image is 100px from viewport
            rootMargin: '100px 0px'
        });
        
        // Target all images with data-src attribute
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
        
        // Convert all img tags to lazyload
        document.querySelectorAll('img:not([data-src])').forEach(img => {
            if (!img.classList.contains('profile-image')) {  // Skip profile images
                // Save the original source
                img.dataset.src = img.src;
                
                // Set a low-quality placeholder if not already set
                if (window.innerWidth <= 768) {  // Only for mobile devices
                    // Only replace the src if we're on slow connections
                    if (navigator.connection && 
                        (navigator.connection.saveData || 
                        ['slow-2g', '2g', '3g'].includes(navigator.connection.effectiveType))) {
                        img.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 150'%3E%3Crect width='300' height='150' fill='%23cccccc'/%3E%3C/svg%3E";
                    }
                    
                    imageObserver.observe(img);
                }
            }
        });
    }
});
