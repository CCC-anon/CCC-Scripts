// ==UserScript==
// @name         Image Preview on Hover with Cursor Follow (Fixed)
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Show an image preview that follows the mouse cursor when hovering over image links, with fixed positioning.
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Function to decode and extract image URL from the query parameters
    const extractImageUrl = (url) => {
        const urlObj = new URL(url);
        const imageUrl = urlObj.searchParams.get('url'); // Assuming 'url' is the query param holding the image link
        return imageUrl ? decodeURIComponent(imageUrl) : null;
    };

    // Preview element
    const preview = document.createElement('img');
    preview.style.position = 'fixed'; // Use fixed to stay in place during scroll
    preview.style.zIndex = 1000; // Ensure it is on top
    preview.style.maxHeight = '300px'; // Max height for the image
    preview.style.border = '1px solid black'; // Border around the image
    preview.style.display = 'none'; // Start hidden
    document.body.appendChild(preview); // Add to the document

    // Function to show the image preview
    const showPreview = (e) => {
        const href = e.target.href; // Get the URL from the link
        const imageUrl = extractImageUrl(href); // Extract and decode the image URL
        if (!imageUrl || !imageUrl.match(/\.(jpeg|jpg|gif|png|svg)$/i)) {
            return; // Ignore if no image or not an image link
        }

        preview.src = imageUrl;
        preview.style.display = 'block'; // Show the preview
        movePreview(e);
    };

    // Function to move the preview with the mouse
    const movePreview = (e) => {
        preview.style.left = `${e.clientX + 15}px`; // 15px to the right of the cursor
        preview.style.top = `${e.clientY + 15}px`; // 15px below the cursor
    };

    // Function to hide the preview
    const hidePreview = () => {
        preview.style.display = 'none'; // Hide the preview
    };

    // Attach event handlers to all links
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('mouseenter', showPreview);
        link.addEventListener('mousemove', movePreview);
        link.addEventListener('mouseleave', hidePreview);
    });
})();
