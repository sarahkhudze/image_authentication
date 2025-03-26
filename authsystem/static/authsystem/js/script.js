document.addEventListener('DOMContentLoaded', function() {
    // Close alert messages after 5 seconds
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Image preview for upload form
    const imageInput = document.getElementById('id_image');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const previewContainer = document.getElementById('image-preview-container');
                if (!previewContainer) {
                    const container = document.createElement('div');
                    container.id = 'image-preview-container';
                    container.className = 'mt-3 text-center';
                    imageInput.parentNode.appendChild(container);
                }
                
                const reader = new FileReader();
                reader.onload = function(event) {
                    const img = document.createElement('img');
                    img.src = event.target.result;
                    img.className = 'img-thumbnail';
                    img.style.maxHeight = '200px';
                    
                    const previewContainer = document.getElementById('image-preview-container');
                    previewContainer.innerHTML = '';
                    previewContainer.appendChild(img);
                };
                reader.readAsDataURL(file);
            }
        });
    }
});