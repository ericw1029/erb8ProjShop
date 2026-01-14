// Mock Data
const menuItems = [
    {
        id: 1,
        name: 'Classic Cheeseburger',
        description: 'Juicy beef patty with cheddar cheese, lettuce, tomato, and our secret sauce.',
        price: 12.99,
        image: 'public/images/burger.jpg',
        category: 'burgers',
        popular: true
    },
    {
        id: 2,
        name: 'Double Bacon Burger',
        description: 'Two beef patties, crispy bacon, caramelized onions, and BBQ sauce.',
        price: 16.99,
        image: 'public/images/burger.jpg',
        category: 'burgers',
        popular: false
    },
    {
        id: 3,
        name: 'Margherita Pizza',
        description: 'Fresh mozzarella, basil, and tomato sauce on a thin crust.',
        price: 14.99,
        image: 'public/images/pizza.jpg',
        category: 'pizza',
        popular: false
    },
    {
        id: 4,
        name: 'Pepperoni Feast',
        description: 'Loaded with pepperoni and extra cheese.',
        price: 18.99,
        image: 'public/images/pizza.jpg',
        category: 'pizza',
        popular: true
    },
    {
        id: 5,
        name: 'Salmon Roll',
        description: 'Fresh salmon, avocado, and cucumber wrapped in seaweed and rice.',
        price: 10.99,
        image: 'public/images/sushi.jpg',
        category: 'sushi',
        popular: false
    },
    {
        id: 6,
        name: 'Spicy Tuna Roll',
        description: 'Tuna mixed with spicy mayo, topped with sesame seeds.',
        price: 11.99,
        image: 'public/images/sushi.jpg',
        category: 'sushi',
        popular: true
    }
];

// State
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let comments = JSON.parse(localStorage.getItem('comments')) || [
    { itemId: 1, name: 'John Doe', rating: 5, text: 'Amazing food! The burger was juicy and delicious.', date: '2023-10-15' },
    { itemId: 3, name: 'Jane Smith', rating: 4, text: 'Great service, but the pizza could be crispier.', date: '2023-10-18' }
];

// DOM Elements
const cartCountEl = document.getElementById('cart-count');
const cartItemsEl = document.getElementById('cart-items');
const cartTotalEl = document.getElementById('cart-total');
const menuContainer = document.getElementById('menu-container');
const commentsListEl = document.getElementById('comments-list');
const commentForm = document.getElementById('comment-form');
const itemDetailsContainer = document.getElementById('item-details-container');
const itemCommentsListEl = document.getElementById('item-comments-list');
const itemCommentForm = document.getElementById('item-comment-form');

// Functions
function updateCartUI() {
    if (cartCountEl) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCountEl.textContent = totalItems;
        cartCountEl.style.display = totalItems > 0 ? 'inline-block' : 'none';
    }

    if (cartItemsEl && cartTotalEl) {
        cartItemsEl.innerHTML = '';
        let total = 0;

        if (cart.length === 0) {
            cartItemsEl.innerHTML = '<p class="text-center text-muted my-4">Your cart is empty.</p>';
        } else {
            cart.forEach(item => {
                total += item.price * item.quantity;
                cartItemsEl.innerHTML += `
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h6 class="mb-0">${item.name}</h6>
                            <small class="text-muted">$${item.price.toFixed(2)} x ${item.quantity}</small>
                        </div>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-secondary" onclick="updateQuantity(${item.id}, -1)">-</button>
                            <button class="btn btn-outline-secondary" onclick="updateQuantity(${item.id}, 1)">+</button>
                            <button class="btn btn-outline-danger" onclick="removeFromCart(${item.id})">&times;</button>
                        </div>
                    </div>
                `;
            });
        }
        cartTotalEl.textContent = `$${total.toFixed(2)}`;
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(id) {
    const item = menuItems.find(i => i.id === id);
    const existingItem = cart.find(i => i.id === id);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ ...item, quantity: 1 });
    }
    
    updateCartUI();
}

function updateQuantity(id, change) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(id);
        } else {
            updateCartUI();
        }
    }
}

function removeFromCart(id) {
    cart = cart.filter(i => i.id !== id);
    updateCartUI();
}

function renderMenu(category = 'all') {
    if (!menuContainer) return;

    const items = category === 'all' 
        ? menuItems 
        : menuItems.filter(item => item.category === category);

    menuContainer.innerHTML = items.map(item => `
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="position-relative">
                    <a href="item.html?id=${item.id}">
                        <img src="${item.image}" class="card-img-top" alt="${item.name}">
                    </a>
                    ${item.popular ? '<span class="badge-popular">Popular</span>' : ''}
                </div>
                <div class="card-body d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <a href="item.html?id=${item.id}" class="text-decoration-none text-dark">
                            <h5 class="card-title hover-primary">${item.name}</h5>
                        </a>
                        <span class="fw-bold text-primary">$${item.price.toFixed(2)}</span>
                    </div>
                    <p class="card-text text-muted small flex-grow-1">${item.description}</p>
                    <button class="btn btn-primary w-100 mt-3" onclick="addToCart(${item.id})">
                        Add to Cart
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function renderComments(targetEl, filterItemId = null) {
    if (!targetEl) return;

    const filteredComments = filterItemId 
        ? comments.filter(c => c.itemId === parseInt(filterItemId))
        : comments;

    if (filteredComments.length === 0) {
        targetEl.innerHTML = '<p class="text-muted text-center py-4">No reviews yet. Be the first to review!</p>';
        return;
    }

    targetEl.innerHTML = filteredComments.map(comment => `
        <div class="comment-card">
            <div class="d-flex justify-content-between mb-2">
                <div>
                    <h6 class="fw-bold mb-0">${comment.name}</h6>
                    ${comment.itemId && !filterItemId ? `<small class="text-muted">on <a href="item.html?id=${comment.itemId}" class="text-decoration-none">${menuItems.find(i => i.id === comment.itemId)?.name || 'Unknown Item'}</a></small>` : ''}
                </div>
                <small class="text-muted">${comment.date}</small>
            </div>
            <div class="rating-stars mb-2">
                ${'★'.repeat(comment.rating)}${'☆'.repeat(5 - comment.rating)}
            </div>
            <p class="mb-0 text-secondary">${comment.text}</p>
        </div>
    `).join('');
}

function handleCommentSubmit(e, itemId = null) {
    e.preventDefault();
    const form = e.target;
    const name = form.querySelector('#comment-name').value;
    const rating = parseInt(form.querySelector('#comment-rating').value);
    const text = form.querySelector('#comment-text').value;

    const newComment = {
        itemId: itemId ? parseInt(itemId) : null,
        name,
        rating,
        text,
        date: new Date().toISOString().split('T')[0]
    };

    comments.unshift(newComment);
    localStorage.setItem('comments', JSON.stringify(comments));
    
    if (itemId) {
        renderComments(itemCommentsListEl, itemId);
    } else {
        renderComments(commentsListEl);
    }
    
    form.reset();
}

function renderItemDetails() {
    if (!itemDetailsContainer) return;

    const urlParams = new URLSearchParams(window.location.search);
    const itemId = parseInt(urlParams.get('id'));
    const item = menuItems.find(i => i.id === itemId);

    if (!item) {
        itemDetailsContainer.innerHTML = '<div class="col-12 text-center py-5"><h3>Item not found</h3><a href="menu.html" class="btn btn-primary mt-3">Back to Menu</a></div>';
        return;
    }

    // Render Item Details
    itemDetailsContainer.innerHTML = `
        <div class="col-md-6 mb-4 mb-md-0">
            <img src="${item.image}" class="img-fluid rounded-3 shadow-sm w-100" alt="${item.name}" style="max-height: 500px; object-fit: cover;">
        </div>
        <div class="col-md-6">
            <div class="ps-md-4">
                ${item.popular ? '<span class="badge bg-primary mb-2">Popular Choice</span>' : ''}
                <h1 class="display-5 fw-bold mb-3">${item.name}</h1>
                <h3 class="text-primary fw-bold mb-4">$${item.price.toFixed(2)}</h3>
                <p class="lead text-muted mb-4">${item.description}</p>
                
                <div class="d-flex gap-3">
                    <button class="btn btn-primary btn-lg px-5" onclick="addToCart(${item.id})">Add to Cart</button>
                    <a href="menu.html" class="btn btn-outline-secondary btn-lg">Back to Menu</a>
                </div>
            </div>
        </div>
    `;

    // Render Comments for this item
    renderComments(itemCommentsListEl, itemId);

    // Setup Comment Form
    if (itemCommentForm) {
        itemCommentForm.addEventListener('submit', (e) => handleCommentSubmit(e, itemId));
    }
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
    
    if (menuContainer) {
        renderMenu();
        // Category Filters
        const filterButtons = document.querySelectorAll('.category-filter');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                filterButtons.forEach(b => b.classList.remove('active', 'btn-dark'));
                filterButtons.forEach(b => b.classList.add('btn-outline-dark'));
                e.target.classList.remove('btn-outline-dark');
                e.target.classList.add('active', 'btn-dark');
                renderMenu(e.target.dataset.category);
            });
        });
    }

    if (commentsListEl) {
        renderComments(commentsListEl);
    }

    if (commentForm) {
        commentForm.addEventListener('submit', (e) => handleCommentSubmit(e));
    }

    if (itemDetailsContainer) {
        renderItemDetails();
    }
});

// Expose functions to global scope
window.addToCart = addToCart;
window.updateQuantity = updateQuantity;
window.removeFromCart = removeFromCart;
