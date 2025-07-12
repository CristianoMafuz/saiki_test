/** 
 * @file frontend/site/script/input_handler.js
 * 
 * @author AndreiCristeli
 * @author victorxaviercosta
 * 
 * @version 0.1
 */

import * as attempt from "./attempt.js"
import * as eg from "./easter_eggs.js"

// TODO: Handle entity_type properly according to user's selection.
const ENTITY_TYPE_PH = "Algorithm"

// Normalizes user's input.
// Returns all input words captalized (Change as needed for the backend database).
function __normalize_input(input){
  let trimmed = input.trim(); // Removes leading and trailing spaces (but not spaces between words).
  return trimmed.toLowerCase();
}

// Event handler for keydown on the input text box
export async function input_keydown(event, input, div_attempts) {
  const user_input = __normalize_input(event.target.value); 
  // console.log(`Nomalized Input: ${user_input}`);

  if (/^[a-zA-z]$/.test(event.key)){ // Using RegExp for validating if entry is a letter.
    // TODO: add suggestion logic.
    // console.log(event.key);
    
  } else if (user_input && event.key === 'Enter') {
      if(user_input === "milvus"){
        eg.showMilvusDialog(); input.value = ''; return;

      } else if (user_input === "pokemon" || user_input === "monkepo"){
        eg.showPokemonDialog(); input.value = ''; return;

      }

      let attempt_rc = await attempt.process_attempt(user_input, div_attempts, ENTITY_TYPE_PH);

        switch (attempt_rc){
          case attempt.ATTEMPT_RC.REPEATED_ANSWER: 
          case attempt.ATTEMPT_RC.NOT_FOUND:
            break;
          case attempt.ATTEMPT_RC.VICTORY: // Win Condition.
            attempt.win_condition(input);

          default:
            input.value = '';
        }
    }
}

// Event handler for when clicking on new game.
export function new_game_click(event, btn) {
  const container = btn.closest(".div_new_game");
  const div_attempts = document.querySelector('.attempts-field');
  attempt.reset_game(container, div_attempts);
}

// Event handler for click on the info button.
export function info_click(event, button) {
  const dialog = document.querySelector('.infoDialog');
  if (dialog) {
    dialog.showModal();
  }  
}

// Event handler for click on the close button of the info dialog.
export function close_info_dialog(event, dialog) {
  if(dialog) {
    dialog.style.animation = 'desvanecer 0.8s ease-out forwards';

    dialog.addEventListener('animationend', function handleClose() {
      dialog.close();
      dialog.style.animation = '';
      dialog.removeEventListener('animationend', handleClose);
    });
  }
}  