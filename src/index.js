import barba from '@barba/core';
import "./scss/main.scss";

barba.init({
    // define a custom function that will prevent Barba
    // from working on links that contains a `prevent` CSS class
    prevent: ({ el }) => el.classList && el.classList.contains('prevent')
});