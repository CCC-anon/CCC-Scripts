// ==UserScript==
// @name         Image URL to Thumbnail Converter with Extension Fix
// @namespace    http://tampermonkey.net/
// @version      0.9
// @description  Convert plaintext image URLs to clickable thumbnails with a toggle, ensuring correct extensions
// @author       CCC-anon
// @match        https://boards.4chan.org/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    let showThumbnails = true;

    const createImageLink = (url) => {
        // Correct the URL to ensure it ends with the proper extension
        url = url.replace(/<wbr>/gi, ''); // Remove any <wbr> tags
        url = url.replace(/(pn|jpe|jp).*?g/gi, (match) => {
            if (match.startsWith('pn')) return 'png';
            if (match.startsWith('jpe')) return 'jpeg';
            if (match.startsWith('jp')) return 'jpg';
        });

        let link = document.createElement('a');
        link.href = url;
        link.target = '_blank';

        let img = document.createElement('img');
        img.src = url;
        img.style.maxWidth = '200px';
        img.style.maxHeight = '200px';
        img.style.margin = '5px';

        link.appendChild(img);
        return link.outerHTML;
    };

    const toggleImages = () => {
        showThumbnails = !showThumbnails;
        document.querySelectorAll('blockquote').forEach(blockquote => {
            let text = blockquote.innerHTML;
            if (showThumbnails) {
                // Convert plain text URLs to image tags
                text = text.replace(urlRegex, (match) => createImageLink(match));
            } else {
                // Convert image tags back to plain text URLs, ensuring URLs are displayed correctly
                text = text.replace(/<a href="([^"]+)"[^>]*><img[^>]+><\/a>/g, '$1');
            }
            blockquote.innerHTML = text;
        });
    };

    const toggleButton = document.createElement('button');
    toggleButton.textContent = 'Toggle Thumbnails';
    toggleButton.style.position = 'fixed';
    toggleButton.style.top = '20px';
    toggleButton.style.right = '20px';
    toggleButton.style.zIndex = '1000';
    toggleButton.onclick = toggleImages;

    document.body.appendChild(toggleButton);

    // Regex to handle URLs and any character sequences up to 'g' after partial extensions
    const urlRegex = /https:\/\/(?:files\.catbox\.moe|litter\.catbox\.moe)\/\S+?\.(pn.*?g|jpe.*?g|jp.*?g)/gi;

    document.querySelectorAll('blockquote').forEach(blockquote => {
        let text = blockquote.innerHTML;
        if (showThumbnails) {
            text = text.replace(urlRegex, (match) => createImageLink(match));
        }
        blockquote.innerHTML = text;
    });
})();
