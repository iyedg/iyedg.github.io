import barba from '@barba/core';
import "./scss/main.scss";

import barbaPrefetch from '@barba/prefetch';

barba.use(barbaPrefetch);
barba.init({
    // define a custom function that will prevent Barba
    // from working on links that contains a `prevent` CSS class
    prevent: ({ el }) => el.classList && el.classList.contains('prevent'),
    transitions: [{
        // Render KaTex
        beforeEnter: (data) => renderMathInElement(document.body),
    }]
});
