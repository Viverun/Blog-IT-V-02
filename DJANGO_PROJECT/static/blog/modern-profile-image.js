// Modern Profile Image Handler with Enhanced Features
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const imageInput = document.getElementById('id_image');
    const profilePreview = document.getElementById('profile-preview');
    const imageWrapper = document.querySelector('.current-image-wrapper');
    const feedbackContainer = document.getElementById('upload-feedback');
    const imageOverlay = document.querySelector('.image-overlay');
    const filenameDisplay = document.getElementById('image-filename');
    const uploadProgress = document.getElementById('upload-progress');
    const profileForm = document.querySelector('form');
    
    if (imageInput && profilePreview) {
        // Make the entire image wrapper clickable to trigger file selection
        if (imageWrapper) {
            imageWrapper.addEventListener('click', function() {
                imageInput.click();
            });
        }
        
        // Also handle click on the overlay specifically
        if (imageOverlay) {
            imageOverlay.addEventListener('click', function(e) {
                e.stopPropagation(); // Prevent multiple triggers
                imageInput.click();
            });
        }
        
        // Handle file selection
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                
                // Clear previous feedback
                if (feedbackContainer) {
                    feedbackContainer.innerHTML = '';
                }
                
                // Validate file size (max 2MB)
                if (file.size > 2 * 1024 * 1024) {
                    showFeedback('error', 'Image is too large (max 2MB)');
                    this.value = '';
                    return;
                }
                
                // Validate file type
                const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
                if (!validTypes.includes(file.type)) {
                    showFeedback('error', 'Invalid file type (use JPG, PNG, GIF, WebP)');
                    this.value = '';
                    return;
                }
                
                // Check image dimensions when loaded
                const img = new Image();
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    img.src = e.target.result;
                    img.onload = function() {
                        // Check if image is reasonably square (within 20% tolerance)
                        const ratio = this.width / this.height;
                        if (ratio < 0.8 || ratio > 1.2) {
                            showFeedback('warning', 'Image not square - might look stretched');
                        }
                        
                        // Update preview image
                        profilePreview.src = e.target.result;
                        
                        // Add selected class to wrapper for styling
                        if (imageWrapper) {
                            imageWrapper.classList.add('selected-new-image');
                            
                            // Add a subtle animation
                            profilePreview.style.transform = 'scale(1.1)';
                            setTimeout(() => {
                                profilePreview.style.transform = 'scale(1)';
                            }, 200);
                        }
                        
                        // Show success feedback
                        showFeedback('success', 'New image selected - click Save to update');
                        
                        // Update filename display
                        updateFilenameDisplay(file.name);
                    };
                };
                
                reader.readAsDataURL(file);
            }
        });
        
        // Handle form submission to show upload progress
        if (profileForm) {
            profileForm.addEventListener('submit', function(e) {
                // Only show progress if an image is selected
                if (imageInput.files && imageInput.files.length > 0) {
                    // Show the progress bar
                    if (uploadProgress) {
                        uploadProgress.style.display = 'block';
                    }
                    
                    // Update feedback to show "Uploading..."
                    showFeedback('info', 'Uploading image...');
                }
            });
        }
    }
    
    // Update the filename display with truncation if needed
    function updateFilenameDisplay(filename) {
        if (filenameDisplay) {
            // Truncate filename if needed
            let displayName = filename;
            if (displayName.length > 20) {
                const extension = displayName.split('.').pop();
                const basename = displayName.substring(0, displayName.lastIndexOf('.'));
                displayName = basename.substring(0, 15) + '...' + extension;
            }
            filenameDisplay.textContent = displayName;
        }
    }
    
    // Utility function to show feedback with different types
    function showFeedback(type, message) {
        if (feedbackContainer) {
            feedbackContainer.innerHTML = '';
            
            const feedbackElement = document.createElement('div');
            
            // Apply appropriate class based on feedback type
            switch(type) {
                case 'success':
                    feedbackElement.className = 'upload-success';
                    feedbackElement.innerHTML = '<i class="fas fa-check-circle"></i>';
                    break;
                case 'error':
                    feedbackElement.className = 'upload-error';
                    feedbackElement.innerHTML = '<i class="fas fa-exclamation-circle"></i>';
                    break;
                case 'warning':
                    feedbackElement.className = 'upload-warning';
                    feedbackElement.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
                    feedbackElement.style.color = '#856404';
                    feedbackElement.style.backgroundColor = '#fff3cd';
                    feedbackElement.style.border = '1px solid #ffeeba';
                    break;
                case 'info':
                    feedbackElement.className = 'upload-info';
                    feedbackElement.innerHTML = '<i class="fas fa-info-circle"></i>';
                    feedbackElement.style.color = '#0c5460';
                    feedbackElement.style.backgroundColor = '#d1ecf1';
                    feedbackElement.style.border = '1px solid #bee5eb';
                    break;
            }
            
            const messageSpan = document.createElement('span');
            messageSpan.textContent = message;
            feedbackElement.appendChild(messageSpan);
            
            feedbackContainer.appendChild(feedbackElement);
        }
    }
    
    // Check URL parameters for feedback messages
    function checkURLForMessages() {
        const urlParams = new URLSearchParams(window.location.search);
        const status = urlParams.get('status');
        
        if (status === 'success') {
            // Show success animation if the form was just submitted successfully
            const completeAnimation = document.createElement('div');
            completeAnimation.className = 'upload-complete-animation';
            completeAnimation.innerHTML = '<i class="fas fa-check"></i>';
            
            if (feedbackContainer) {
                feedbackContainer.innerHTML = '';
                feedbackContainer.appendChild(completeAnimation);
                
                const successMessage = document.createElement('div');
                successMessage.className = 'upload-success';
                successMessage.innerText = 'Profile updated successfully!';
                
                // Add a small delay to make animation more noticeable
                setTimeout(() => {
                    feedbackContainer.appendChild(successMessage);
                }, 400);
            }
        }
    }
    
    // Call the URL checker after page load
    checkURLForMessages();
    
    // Add touch device detection and special handling
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    if (isTouchDevice && imageWrapper) {
        // On touch devices, show overlay briefly on page load to indicate it's interactive
        setTimeout(() => {
            imageOverlay.style.opacity = '0.7';
            setTimeout(() => {
                imageOverlay.style.opacity = '0';
            }, 1500);
        }, 500);
        
        // Add a tooltip or hint for touch users
        const touchHint = document.createElement('div');
        touchHint.className = 'touch-hint';
        touchHint.textContent = 'Tap to change image';
        touchHint.style.position = 'absolute';
        touchHint.style.bottom = '-30px';
        touchHint.style.left = '0';
        touchHint.style.right = '0';
        touchHint.style.textAlign = 'center';
        touchHint.style.fontSize = '0.8rem';
        touchHint.style.color = '#666';
        imageWrapper.appendChild(touchHint);
    }
});
