/** 
 * @file frontend/site/scripts/renderer.js
 * 
 * @author victorxaviercosta
 * @author HexagonalUniverse
 * 
 * @version 0.1
 */

import { InputHandler } from "./input_handler.js"

export class Renderer {
	constructor(){
		this.input_handler = new InputHandler(this);
	}

	#render_katex(input_str, target_element) {
		katex.render(input_str, target_element, { 
			diplayMode: true, throwOnError: false
		});  
	}

	#render_math(field, input_list, target_element) {
		if (field === "average_time_complexity") {
			this.#render_katex("T \\in " + input_list, target_element);
		
		} else if (field === "auxiliary_space_complexity") {
			this.#render_katex("S \\in " + input_list, target_element);
		  
		} else {
			for (let value of input_list) {
			  target_element.textContent = target_element.textContent + `${value}\n`;
			}
		}
	}

	render_card(card_object) {
		/**
		 *  Card object must have the fields:
		 * 	name (string)
		 * 	guessed (string)
		 *  data ( {key (string): value (string)} )
		 */

		let card_class = `card ${card_object.guessed}`;
	
		// Creating the card div element.
		const card = document.createElement('div');
		card.className = card_class;
		
		// Creating the card header div element.
		const header = document.createElement('div');
		header.className = "card-header";
		header.textContent = card_object.name;
		card.appendChild(header);
		
		// Creating infoGrid div element.
		const infoGrid = document.createElement('div');
		infoGrid.className = 'info-grid';
		
		// Adding attributes elements.
		for (let key in card_object.data) {
			const infoItem = document.createElement('div');
			
			infoItem.className = `info-item ${card_object.data[key][1]}-color`;
			
			this.#render_math(key, card_object.data[key][0], infoItem);
			infoGrid.appendChild(infoItem);
		}
		
		// Adding info-grid to card
		card.appendChild(infoGrid);
		
		// Insert the card to body ou em outro container (ex: abaixo do último card)
		const container = document.querySelector('.cards-container');
		container.insertBefore(card, container.firstChild);
	}

	remove_hints_container(input_hint_div) {
		let hints_container = document.querySelector(".hints");
	
		if (hints_container) { 
			try {
				hints_container.remove();
				//input_hint_div.removeChild(hints_container);

			} catch (NotFoundError) {
				console.log(`[ERROR]: Unnable to remove hints container: \n ${NotFoundError}`);
			}
		}
	}

	/** Renders the hints at the input text-box. */
	render_hints(hints, selected) {
		const input_hint_div = document.querySelector(".input-hint");
		
		this.remove_hints_container(input_hint_div);
		
		if (hints.length == 0)
			return;
		
		// re-creating hints container.
		let hints_container = document.createElement('div');
		hints_container.className = "hints"

		// console.log(`selected = ${selected}`);
		
		// adding each hint row.
		for (let name of hints) {
			// each hint row...
			const hint_item = document.createElement('div');
			hint_item.className = "hint_item";

			if (name == hints[selected]) {
				hint_item.className = hint_item.className + " selected";
				// console.log(`selected name = ${name}`);
			}

			hint_item.innerText = name;
			hint_item.addEventListener('click', (event) => this.input_handler.hint_click(event, hint_item));
			hint_item.addEventListener('mouseenter', (event) => {
    			hint_item.className = hint_item.className + " selected";
			})
			hint_item.addEventListener('mouseleave', (event) => {
    			hint_item.className = "hint_item";
			})
			hints_container.appendChild(hint_item);
		}
		
		input_hint_div.appendChild(hints_container);
	}

	update_hints(hints, selected){
		const hints_container = document.querySelector('.hints');
		// console.log(`Updating hints container`);

		// adding each hint row.
		for (let child of hints_container.childNodes) {
			// each hint row...
			child.className = "hint_item";
			
			if (child.innerText == hints[selected]) {
				child.className = child.className + " selected"
				// console.log(`new selected name = ${child.innerText}`);
			}
		}
	}

	/** Bulk-loads a collection of entities.
	 *  Used on page-refresh, for maintaining the visual information of the game-state. */
	render_collection(entities) {
		// console.log("entities:", entities);
	
		// iteratively rendering each card, in order...
		for (let entity of entities) {
			this.render_card(entity);
		}
	}
}