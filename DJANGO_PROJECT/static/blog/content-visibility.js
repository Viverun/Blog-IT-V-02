// Improved content visibility management - No fade, only slide animation
document.addEventListener('DOMContentLoaded', function() {
  const sections = document.querySelectorAll('.content-section');

  // Immediately make all content visible and set its final resting state.
  sections.forEach(section => {
    section.style.opacity = '1';
    section.style.visibility = 'visible';
    section.style.transform = 'translateY(0)';
  });
  
  const isSlowConnection = navigator.connection && 
    (navigator.connection.saveData || 
    ['slow-2g', '2g', '3g'].includes(navigator.connection.effectiveType));
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  // Skip animations for accessibility, slow connections, or if IntersectionObserver is not supported.
  if (prefersReducedMotion || isSlowConnection || !('IntersectionObserver' in window)) {
    if (!('IntersectionObserver' in window)) {
      console.log('IntersectionObserver not supported, skipping animations.');
    } else {
      console.log('Skipping animations due to preferences or connection.');
    }
    return; // Content remains as set above (fully visible, no transform animation).
  }
  
  // Define animation style - opacity part will be unused if opacity is always 1.
  const animationStyle = 'opacity 0.5s ease, transform 0.5s ease'; 
  
  // Use a timeout to allow initial rendering and then apply starting animation state.
  setTimeout(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const target = entry.target;
        if (entry.isIntersecting) {
          // Animate to final state (transform back to 0)
          // Opacity is already 1 and stays 1.
          target.style.transform = 'translateY(0)';
          // target.style.transition is already set.
          observer.unobserve(target);
        }
      });
    }, { 
      threshold: 0.1, // When 10% of the element is visible
      rootMargin: "0px" 
    });

    sections.forEach(section => {
      // Prepare for slide animation. Content is already opacity:1, visibility:visible.
      // Set the starting position for the transform.
      section.style.transform = 'translateY(20px)'; // Start slightly down
      section.style.transition = animationStyle; // Apply transition styles
      observer.observe(section);
    });
  }, 100); // 100ms delay
});
