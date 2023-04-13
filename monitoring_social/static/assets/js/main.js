/******/ (function() { // webpackBootstrap
/******/ 	"use strict";
var __webpack_exports__ = {};

;// CONCATENATED MODULE: ./assets_src/ts/modules/menu.ts
const menu = document.querySelector('.js_left_menu');
const closeMenu = document.querySelector('.js_close_menu');
console.log(1);
closeMenu.addEventListener('click', el => {
  console.log(2);
  menu.classList.toggle('show');
  closeMenu.classList.toggle('open');
});

;// CONCATENATED MODULE: ./assets_src/ts/app.ts

/******/ })()
;