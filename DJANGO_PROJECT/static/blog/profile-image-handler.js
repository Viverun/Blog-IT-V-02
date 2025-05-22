// Profile image upload handling
document.addEventListener('DOMContentLoaded', function() {
    // Get image upload input element
    const imageInput = document.getElementById('id_image');
    
    if (imageInput) {
        // Current image preview
        const currentImage = document.querySelector('.current-profile-image-display img');
        
        // Add change event listener to handle preview
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                
                // Check file size (max 2MB)
                if (file.size > 2 * 1024 * 1024) {
                    alert('File is too large! Maximum size is 2MB.');
                    this.value = '';
                    return;
                }
                
                // Check file type
                const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
                if (!validTypes.includes(file.type)) {
                    alert('Invalid file type! Please upload a JPG, PNG, GIF, or WebP image.');
                    this.value = '';
                    return;
                }
                
                // Show preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    currentImage.src = e.target.result;
                    
                    // Add visual feedback
                    currentImage.style.borderColor = '#28a745';
                    currentImage.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.25)';
                    
                    // Add label to indicate upload pending
                    const statusLabel = document.createElement('div');
                    statusLabel.classList.add('upload-pending-badge');
                    statusLabel.innerHTML = '<i class="fas fa-check-circle"></i> Image selected (click Save to update)';
                    
                    // Remove existing label if any
                    const existingLabel = document.querySelector('.upload-pending-badge');
                    if (existingLabel) {
                        existingLabel.remove();
                    }
                    
                    // Add label near the image
                    const imageContainer = document.querySelector('.current-profile-image-display');
                    imageContainer.appendChild(statusLabel);
                };
                
                reader.readAsDataURL(file);
            }
        });
    }
});
