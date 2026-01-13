# E-Restaurant Frontend (HTML/JS/Bootstrap)

This is a simple, static frontend for an e-restaurant application, built with HTML5, Bootstrap 5, and Vanilla JavaScript.

## Features

- **Home Page**: Hero section and featured categories.
- **Menu Page**: Dynamic menu listing with category filtering.
- **Comments Page**: Customer review system with local storage persistence.
- **Cart System**: Modal-based cart with add/remove functionality (persisted in local storage).
- **Responsive Design**: Fully responsive using Bootstrap grid system.

## Tech Stack

- **HTML5**: Semantic markup.
- **CSS3**: Bootstrap 5 + Custom styles (`css/style.css`).
- **JavaScript**: Vanilla JS (`js/app.js`) for logic.

## Project Structure

- `index.html`: Landing page.
- `menu.html`: Menu page.
- `comments.html`: Customer comments page.
- `js/app.js`: Application logic (Cart, Menu rendering, Comments).
- `css/style.css`: Custom styling.
- `public/images`: Static assets.

## How to Run

Simply open `index.html` in your web browser. No build step required.

## Backend Integration

This version uses mock data defined in `js/app.js`. To integrate with a Django backend:

1.  Replace the `menuItems` array in `js/app.js` with a `fetch()` call to your API.
2.  Update `handleCommentSubmit` to POST data to your backend instead of saving to localStorage.
