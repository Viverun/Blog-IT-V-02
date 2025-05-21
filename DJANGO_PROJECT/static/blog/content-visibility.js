// Improved content visibility management
document.addEventListener('DOMContentLoaded', function() {
  // Immediately make all content visible first (as a fallback)
  document.querySelectorAll('.content-section').forEach(section => {
    section.style.opacity = '1';
    section.style.visibility = 'visible';
    section.style.transform = 'translateY(0)';
  });
  
  // Check if we're on a slow connection
  const isSlowConnection = navigator.connection && 
    (navigator.connection.saveData || 
    ['slow-2g', '2g', '3g'].includes(navigator.connection.effectiveType));
  
  // Respect reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  // Skip animations for accessibility or slow connections
  if (prefersReducedMotion || isSlowConnection) { // Removed isMobile check
    console.log('Skipping animations due to preferences or connection');
    return;
  }
  
  // For mobile devices, use simpler animations
  const animationStyle = 'opacity 0.5s ease, transform 0.5s ease'; // Removed isMobile ternary
  
  // Only use the fancy animations if we have IntersectionObserver and not in Save Data mode
  if ('IntersectionObserver' in window) {
    // Use a timeout to ensure content is already visible before applying animations
    setTimeout(() => {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            // Smoothly fade in
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        });
      }, { 
        threshold: 0.1, // Removed isMobile ternary
        rootMargin: "0px" // Removed isMobile ternary
      });
      
      const contentSections = Array.from(document.querySelectorAll('.content-section'));
      // const animatedSections = isMobile ? contentSections.slice(0, 5) : contentSections; // Removed isMobile logic
      
      contentSections.forEach(section => { // Changed animatedSections to contentSections
        // Make sure the section is visible first (accessibility)
        section.style.opacity = '0.1'; // Start slightly visible for accessibility
        section.style.visibility = 'visible';
        section.style.transform = 'translateY(20px)'; // Removed isMobile ternary
        section.style.transition = animationStyle;
        observer.observe(section);
      });
      
      // Make remaining sections visible immediately on mobile - REMOVED
      // if (isMobile && contentSections.length > 5) { 
      //   contentSections.slice(5).forEach(section => {
      //     section.style.opacity = '1';
      //     section.style.visibility = 'visible';
      //   });
      // }
    }, 100); // Small delay to ensure content is visible first
  }
});
