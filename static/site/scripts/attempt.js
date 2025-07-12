/** 
 * @file frontend/site/script/attempt.js
 * 
 * @author AndreiCristeli
 * @author victorxaviercosta
 * 
 * @version 0.1
 */

import { api } from "./api.js"
import { input_keydown, new_game_click } from "./input_handler.js"; 

let number_attempts = 0; // Temporaly saved as a global shared variable.
let victory = false; // Temporaly saved as a global shared variable.
// TODO: Structure a frontend Player data-structure.

import { render_card } from "./renderer.js"

export const ATTEMPT_RC = {
    SUCCESS: 0,
    REPEATED_ANSWER: 1,
    NOT_FOUND: 2,
    VICTORY: 3
};

async function __backend_attempt(user_input, entity_type){
    // Search in database passing entity_type and user_input.

    let attempt;
    try{
        attempt = await api("/guess/entity/", "POST", { entity : user_input });
    } catch(error){
        console.log(error);
    }

    return attempt;
}

export function verify_repeat(user_input){
    const card_container = document.querySelector('.cards-container');

    for(let card of card_container.children){
        if(card.querySelector(".card-header").textContent.toLowerCase() === user_input){
            return true;
        }
    }

    return false;
}

export async function process_attempt(user_input, div_attempts, entity_type){
    if (verify_repeat(user_input)){
        return ATTEMPT_RC.REPEATED_ANSWER;
    }

    // Call back_end attempt process_logic.
    let attempt = await __backend_attempt(user_input, entity_type);
    if(Object.keys(attempt).length === 0) {
        return ATTEMPT_RC.NOT_FOUND; // Entity not found in db.
    }

    // TODO: Treat invalid entry case.
    // Idea: Only call process_attempt if there's a 'first suggestion' when Suggestion is implemented.

    // Updating attempt count.
    number_attempts++;
    div_attempts.textContent = `${number_attempts}`;
    
    // Get player victory logic from backend.
    let card_class = `card ${attempt.type}`;
    console.log(`Card Class = ${card_class}`);

    // Add a new card corresponding to user's attempt.
    
    render_card(attempt, card_class);

    if(attempt.type === "correct"){
        victory = true;
        return ATTEMPT_RC.VICTORY;
    }

    return ATTEMPT_RC.SUCCESS;
}

export function win_condition(input) {
  input.disabled = true;

  /*
  Diary mode
  input.style.border = "2px solid green";
  input.style.backgroundColor = "#e0ffe0";
  input.style.color = "#004400";
  input.placeholder = "Parabéns! Você venceu! 🎉";
  */

  const div = document.createElement("div");
  div.textContent = "Parabéns! Você venceu! 🎉";
  div.className = "div_new_game"; // Se quiser estilizar com CSS

  const btn = document.createElement("button");
  btn.textContent = "Novo Jogo";
  btn.className = "btn_new_game";
  btn.addEventListener("click", (event) => new_game_click(event, btn));

  // Adicionar o botão à div
  div.appendChild(btn);
  input.parentNode.replaceChild(div, input);
}

export function reset_game(container, div_attempts) {
  const new_input = document.createElement("input");
  new_input.type = "text";
  new_input.className = "Input";
  new_input.placeholder = "Escreva aqui";
  new_input.autocomplete = "off";

  container.parentNode.replaceChild(new_input, container);

  // Resetar variáveis de controle
  number_attempts = 0;
  victory = false;

  if (div_attempts) {
    div_attempts.textContent = `${number_attempts}`;
  }

  const cardsContainer = document.querySelector(".cards-container");
  if (cardsContainer) {
    cardsContainer.innerHTML = "";
  }

  new_input.disabled = false;
  new_input.value = "";

  new_input.addEventListener("keydown", (event) =>
    input_keydown(event, new_input, div_attempts)
  );

  // Se houver função para iniciar jogo, chame aqui:
  // start_new_game();
}
