// Improved content visibility management
document.addEventListener('DOMContentLoaded', function() {
  // Immediately make all content visible first (as a fallback)
  document.querySelectorAll('.content-section').forEach(section => {
    section.style.opacity = '1';
    section.style.transform = 'translateY(0)';
  });
  
  // Check if we're on mobile
  const isMobile = window.innerWidth <= 768;
  
  // Check if we're on a slow connection
  const isSlowConnection = navigator.connection && 
    (navigator.connection.saveData || 
    ['slow-2g', '2g', '3g'].includes(navigator.connection.effectiveType));
  
  // Skip animations on mobile devices with slow connections
  if (isMobile && isSlowConnection) {
    console.log('Skipping animations on slow mobile connection');
    return;
  }
  
  // Only use the fancy animations if we have IntersectionObserver and not in Save Data mode
  if ('IntersectionObserver' in window) {
    // Use a timeout to ensure content is already visible before applying animations
    setTimeout(() => {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('show');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });
      
      document.querySelectorAll('.content-section').forEach(section => {
        // Only apply animation when page fully loaded
        if (document.readyState === 'complete') {
          section.style.opacity = '0';
          section.style.transform = 'translateY(20px)';
          section.style.transition = 'opacity 0.5s, transform 0.5s';
          observer.observe(section);
        }
      });
    }, 100); // Small delay to ensure content is visible first
  }
});
