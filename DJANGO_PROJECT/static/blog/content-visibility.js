// Fixed content visibility management - No opacity fade, content always visible
document.addEventListener('DOMContentLoaded', function() {
  const sections = document.querySelectorAll('.content-section');

  // Immediately make all content fully visible and keep it that way
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
      console.log('IntersectionObserver not supported, content remains visible.');
    } else {
      console.log('Animations disabled for user preferences, content remains visible.');
    }
    return; // Content remains fully visible with no animations
  }
  
  // Animation only affects transform (slide), never opacity
  const animationStyle = 'transform 0.5s ease'; 
  
  // Apply slide animation after initial render
  setTimeout(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const target = entry.target;
        if (entry.isIntersecting) {
          // Slide animation to final position - opacity stays 1
          target.style.transform = 'translateY(0)';
          observer.unobserve(target);
        }
      });
    }, { 
      threshold: 0.1,
      rootMargin: "0px" 
    });

    sections.forEach(section => {
      // Set starting slide position - opacity remains 1 always
      section.style.transform = 'translateY(20px)';
      section.style.transition = animationStyle;
      observer.observe(section);
    });
  }, 100);
});
