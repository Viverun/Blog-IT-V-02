// Enhanced profile image handler
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const imageInput = document.getElementById('id_image');
    const profilePreview = document.getElementById('profile-preview');
    const feedbackContainer = document.getElementById('upload-feedback');
    const imageOverlay = document.querySelector('.image-overlay');
    
    if (imageInput && profilePreview) {
        // Click on image overlay should trigger file input
        if (imageOverlay) {
            imageOverlay.addEventListener('click', function() {
                imageInput.click();
            });
        }
        
        // Handle file selection
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                
                // Validate file size (max 2MB)
                if (file.size > 2 * 1024 * 1024) {
                    showFeedback('error', 'Image is too large (max 2MB)');
                    this.value = '';
                    return;
                }
                
                // Validate file type
                const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
                if (!validTypes.includes(file.type)) {
                    showFeedback('error', 'Invalid file type (use JPG, PNG, GIF)');
                    this.value = '';
                    return;
                }
                
                // Show preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Update image preview
                    profilePreview.src = e.target.result;
                    profilePreview.parentElement.classList.add('selected-new-image');
                    
                    // Show success feedback
                    showFeedback('success', 'New image selected - click Save to update');
                    
                    // Update image name badge if it exists
                    const nameElement = document.querySelector('.image-name-badge span');
                    if (nameElement) {
                        // Truncate filename if needed
                        let displayName = file.name;
                        if (displayName.length > 20) {
                            displayName = displayName.substring(0, 17) + '...';
                        }
                        nameElement.textContent = displayName;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Utility function to show feedback
    function showFeedback(type, message) {
        if (feedbackContainer) {
            feedbackContainer.innerHTML = '';
            
            const feedbackElement = document.createElement('div');
            feedbackElement.className = type === 'success' ? 'upload-success' : 'upload-error';
            
            const icon = document.createElement('i');
            icon.className = type === 'success' 
                ? 'fas fa-check-circle' 
                : 'fas fa-exclamation-circle';
            
            const messageSpan = document.createElement('span');
            messageSpan.textContent = message;
            
            feedbackElement.appendChild(icon);
            feedbackElement.appendChild(messageSpan);
            feedbackContainer.appendChild(feedbackElement);
        }
    }
});
