// Modified lazy loading - No opacity animations, immediate content visibility
document.addEventListener('DOMContentLoaded', function() {
    // Immediately show all images to prevent content fading
    document.querySelectorAll('img[data-src]').forEach(img => {
        // Replace the src with the data-src immediately
        if (img.dataset.src) {
            img.src = img.dataset.src;
        }
        
        // Replace srcset if available
        if (img.dataset.srcset) {
            img.srcset = img.dataset.srcset;
        }
        
        // Make sure image is visible
        img.style.opacity = '1';
        img.style.visibility = 'visible';
    });
    
    // Regular images too
    document.querySelectorAll('img:not([data-src])').forEach(img => {
        img.style.opacity = '1';
        img.style.visibility = 'visible';
    });
    
    console.log('Lazy loading disabled - all images loaded immediately');
});
                
                // Set a low-quality placeholder if not already set
                // Only replace the src if we're on slow connections
                if (navigator.connection && 
                    (navigator.connection.saveData || 
                    ['slow-2g', '2g', '3g'].includes(navigator.connection.effectiveType))) {
                    img.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 150'%3E%3Crect width='300' height='150' fill='%23cccccc'/%3E%3C/svg%3E";
                }
                
                imageObserver.observe(img);
            }
        });
    }
});
