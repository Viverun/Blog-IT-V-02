/**
 * Debug script to prevent any element from becoming invisible 
 * and log attempts to hide elements
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Visibility debugger activated - monitoring DOM for visibility changes');
    
    // Function to keep everything visible
    function forceVisibility() {
        // Ensure all elements are visible
        const allElements = document.querySelectorAll('*');
        
        allElements.forEach(el => {
            // Get computed style
            const style = window.getComputedStyle(el);
            
            // Check if element is being hidden
            if (style.opacity < 1 || 
                style.visibility === 'hidden' || 
                style.display === 'none') {
                
                console.warn('Element attempting to hide:', el);
                console.warn('Current styles:', {
                    opacity: style.opacity,
                    visibility: style.visibility,
                    display: style.display
                });
                
                // Force visibility
                el.style.opacity = '1';
                el.style.visibility = 'visible';
                
                // Only change display if it's none
                if (style.display === 'none') {
                    el.style.display = 'block';
                }
            }
        });
    }
    
    // Run immediately
    forceVisibility();
    
    // Run every 500ms to catch any dynamic changes
    setInterval(forceVisibility, 500);
    
    // Also create a MutationObserver to monitor DOM changes
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.type === 'attributes' && 
                (mutation.attributeName === 'style' || 
                 mutation.attributeName === 'class')) {
                
                const target = mutation.target;
                const style = window.getComputedStyle(target);
                
                // Check if element is trying to become invisible
                if (style.opacity < 1 || 
                    style.visibility === 'hidden' || 
                    style.display === 'none') {
                    
                    console.warn('Dynamic change attempting to hide element:', target);
                    console.warn('Changed attribute:', mutation.attributeName);
                    
                    // Force visibility
                    target.style.opacity = '1';
                    target.style.visibility = 'visible';
                    
                    // Only change display if it's none
                    if (style.display === 'none' && 
                        !target.classList.contains('d-none') && // Avoid breaking Bootstrap
                        !target.classList.contains('collapse')) { // Avoid breaking collapsible elements
                        target.style.display = 'block';
                    }
                }
            }
        });
    });
    
    // Start observing the entire document
    observer.observe(document.body, {
        attributes: true,
        childList: true,
        subtree: true,
        attributeFilter: ['style', 'class']
    });
});
