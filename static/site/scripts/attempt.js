/** 
 * @file frontend/site/scripts/attempt.js
 * 
 * @author AndreiCristeli
 * @author victorxaviercosta
 * @author HexagonalUniverse
 * 
 * @version 0.2
 */

import { api } from "./api.js"
// import { InputHandler } from "./input_handler.js"; 
import { Renderer } from "./renderer.js"

// TODO: Structure a frontend Player data-structure.

/** Return Codes for the attempts processing */
export const ATTEMPT_RC = {
    SUCCESS: 0,         // Attempt successfully processed.
    REPEATED_ANSWER: 1, // The attempt is a repeated entry.
    NOT_FOUND: 2,       // Entity not found in db.
    VICTORY: 3,         // The attempt result's in player's Victory.
};

export class AttemptsHandler {
    constructor(renderer){
        this.number_attempts = 0;
        this.div_attempts = document.querySelector('.attempts-field');

        this.renderer = renderer
    }

    /** Updates the attempts count variable as well as the page's attempts counter element. */
    #attempt_count_update() {
        ++ this.number_attempts;
        this.div_attempts.textContent = `${this.number_attempts}`;
    }
    
    /** Loads the attempt game state screen. 
        Called on page-show. */
    load_game_state_screen(event, __on_load_response) {
        this.renderer.render_collection(__on_load_response["entities"]);
        this.number_attempts = __on_load_response["tries"] - 1;
    
        this.#attempt_count_update();
    }

    /** Executes a backend attempt request and gets it's response */
    async #__backend_attempt(user_input, entity_type) {
        // Search in database passing entity_type and user_input.
    
        let attempt;
        try{
            attempt = await api("/guess/entity/", "POST", { entity : user_input });
        } catch(error){
            console.log(error);
        }
    
        return attempt;
    }

    /** Verifies possible repeated entry by the user */
    verify_repeat(user_input){
        const card_container = document.querySelector('.cards-container');
        
        // Sequentially verifying if there's any card matching user's input.
        for(let card of card_container.children){
            if(card.querySelector(".card-header").textContent.toLowerCase() === user_input){
                return true;
            }
        }
    
        return false;
    }
    
    /** Handles all the attempt processing logic. */
    async process_attempt(user_input, entity_type){
        if (this.verify_repeat(user_input)){
            return ATTEMPT_RC.REPEATED_ANSWER;
        }
    
        let attempt = await this.#__backend_attempt(user_input, entity_type);
    
        // Validating Backend's response.
        if(Object.keys(attempt).length === 0) {
            return ATTEMPT_RC.NOT_FOUND;
        }
    
        // TODO: Treat invalid entry case.
        // Idea: Only call process_attempt if there's a 'first suggestion' when Suggestion is implemented.
    
        // Incrementing attempts counter.
        this.#attempt_count_update(this.div_attempts);
    
        // Adding a new card corresponding to user's attempt.
        this.renderer.render_card(attempt);
    
        // Validating player's victory.
        if (attempt.guessed === "correct") {
            return ATTEMPT_RC.VICTORY;
        }
        
        return ATTEMPT_RC.SUCCESS;
    }
}