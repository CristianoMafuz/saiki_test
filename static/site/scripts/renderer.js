/** 
 * @file frontend/site/scripts/renderer.js
 * 
 * @author victorxaviercosta
 * 
 * @version 0.1
 */

function render_katex(input_str, target_element) {
    katex.render(input_str, target_element, { 
      diplayMode: true, throwOnError: false
    });  
}

function render_math(field, input_str, target_element) {

    if (field === "average_time_complexity") {
        render_katex("T \\in " + input_str, target_element);
      
    } else if (field === "auxiliary_space_complexity") {
        render_katex("S \\in " + input_str, target_element);
      
    } else {
        target_element.textContent = input_str;
    }
}

export function render_card(object, card_class){
  // Creating the card div element.
  const card = document.createElement('div');
  card.className = card_class;
  
  // Creating the card header div element.
  const header = document.createElement('div');
  header.className = "card-header";
  header.textContent = object.name;
  card.appendChild(header);

  // Creating infoGrid div element.
  const infoGrid = document.createElement('div');
  infoGrid.className = 'info-grid';

  // Adding attributes elements.
  for (let key in object.data) {
    const infoItem = document.createElement('div');
    
    infoItem.className = `info-item ${object.data[key][1]}-color`;
    
    render_math(key, object.data[key][0], infoItem);
    infoGrid.appendChild(infoItem);
  }

  // Adding info-grid to card
  card.appendChild(infoGrid);
  
  // Insert the card to body ou em outro container (ex: abaixo do último card)
  const container = document.querySelector('.cards-container');
  container.insertBefore(card, container.firstChild);
}