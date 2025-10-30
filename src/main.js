import { galleryItems } from "./images.js";



// DOM elements
const gallery = document.querySelector('.gallery');
const filterButtons = document.querySelectorAll('.filter-btn');
const lightbox = document.querySelector('.lightbox');
const lightboxImg = document.querySelector('.lightbox-img');
const lightboxCaption = document.querySelector('.lightbox-caption');
const closeBtn = document.querySelector('.close-btn');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

// Current image index for lightbox navigation
let currentImageIndex = 0;

// Initialize gallery
function initGallery() {
    displayGalleryItems(galleryItems);

    // Filter functionality
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Filter items
            const filter = button.getAttribute('data-filter');
            if (filter === 'all') {
                displayGalleryItems(galleryItems);
            } else {
                const filteredItems = galleryItems.filter(item => item.category === filter);
                displayGalleryItems(filteredItems);
            }
        });
    });
}

// Display gallery items
function displayGalleryItems(items) {
    gallery.innerHTML = '';

    items.forEach((item, index) => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';
        galleryItem.setAttribute('data-category', item.category);
        galleryItem.setAttribute('data-index', index);

        galleryItem.innerHTML = `
                    <img src="${item.src}" alt="${item.title}">
                    <div class="caption">
                        <h3>${item.title}</h3>
                        <p>${item.description}</p>
                    </div>
                `;

        // Add click event to open lightbox
        galleryItem.addEventListener('click', () => {
            openLightbox(items, index);
        });

        gallery.appendChild(galleryItem);
    });
}

// Open lightbox
function openLightbox(items, index) {
    currentImageIndex = index;
    updateLightbox(items);
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}

// Update lightbox content
function updateLightbox(items) {
    const item = items[currentImageIndex];
    lightboxImg.src = item.src;
    lightboxCaption.textContent = `${item.title} - ${item.description}`;
}

// Close lightbox
function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = 'auto'; // Re-enable scrolling
}

// Navigate to previous image
function prevImage(items) {
    currentImageIndex = (currentImageIndex - 1 + items.length) % items.length;
    updateLightbox(items);
}

// Navigate to next image
function nextImage(items) {
    currentImageIndex = (currentImageIndex + 1) % items.length;
    updateLightbox(items);
}

// Event listeners
closeBtn.addEventListener('click', closeLightbox);

prevBtn.addEventListener('click', () => {
    const activeFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
    const items = activeFilter === 'all' ? galleryItems : galleryItems.filter(item => item.category === activeFilter);
    prevImage(items);
});

nextBtn.addEventListener('click', () => {
    const activeFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
    const items = activeFilter === 'all' ? galleryItems : galleryItems.filter(item => item.category === activeFilter);
    nextImage(items);
});

// Close lightbox when clicking outside the image
lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
        closeLightbox();
    }
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('active')) return;

    const activeFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
    const items = activeFilter === 'all' ? galleryItems : galleryItems.filter(item => item.category === activeFilter);

    if (e.key === 'Escape') {
        closeLightbox();
    } else if (e.key === 'ArrowLeft') {
        prevImage(items);
    } else if (e.key === 'ArrowRight') {
        nextImage(items);
    }
});


// Initialize the gallery when page loads
window.addEventListener('DOMContentLoaded', initGallery);
