// Static content visibility - No animations, content always fully visible
document.addEventListener('DOMContentLoaded', function() {
  const sections = document.querySelectorAll('.content-section');

  // Simply make all content fully visible - no animations whatsoever
  sections.forEach(section => {
    // Force immediate full visibility with no transitions or animations
    section.style.opacity = '1';
    section.style.visibility = 'visible';
    section.style.transform = 'none';
    section.style.transition = 'none';
    
    // Ensure content can't be hidden by other means
    section.style.display = 'block';
    section.style.contentVisibility = 'auto';
  });
  
  // Log to console for debugging
  console.log('All animations disabled, content set to permanently visible');
});
