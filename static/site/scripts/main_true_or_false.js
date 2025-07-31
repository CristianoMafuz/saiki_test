/** 
 * @file 	frontend/site/scripts/main_true_or_false.js
 * 
 * @author 	AndreiCristeli
 * @author 	victorxaviercosta
 * 
 * @version 0.2
 */

import { Renderer } from "./renderer.js";
import { api } from "./api.js";

let renderer = new Renderer()

window.onload = function () {
	const currentPage = document.body.dataset.page;

	const menuItems = document.querySelectorAll(".menu-item");

	menuItems.forEach(item => {
		if (item.dataset.page === currentPage) {
			item.classList.add("active");
		} else {
			item.classList.remove("active"); // útil se for SPA
		}
	});

  const button = document.querySelector('.footer-info');
	button.addEventListener('click', (event) => renderer.input_handler.info_click(event, button));

  const buttons = document.querySelectorAll('.button_choice');
  buttons.forEach(button => {
    button.addEventListener('click', (event) => renderer.input_handler.choice_click(event, button));
  });

  const closeBtn = document.querySelector('.closeDialog');
  if (closeBtn) {
    const dialog = document.querySelector('.infoDialog');
    closeBtn.addEventListener('click', (event) => renderer.input_handler.close_info_dialog(event, dialog));
  }
};
