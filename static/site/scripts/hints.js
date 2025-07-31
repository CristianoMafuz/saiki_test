/** 
 * @file frontend/site/scripts/hints.js
 * 
 * @author victorxaviercosta
 * @author HexagonalUniverse
 * 
 * @version 0.2
 */

import { Renderer } from "./renderer.js";
import { api } from "./api.js";

export class Hints {
    #displaying;

    constructor(renderer){
        this.renderer = renderer

        this.the_hints = [];
        this.selected_hint_index = 0;

        this.#displaying = false;
    }
    
    is_displaying(){
        return this.#displaying;
    }

    /** Handles backend hints request returning the backend's offered list of suggestions */
    async __get_backend_hints(input) {
        let response;
        try {
            response = await api("/guess/hint/", "POST", { "attempt": `${input}` });
            
        } catch(error) {
            console.log(error);
        }
        
        return response['closest_matches'];
    }

    /** Hides the hint's div element (Removing it) */
    hide(){
        this.renderer.remove_hints_container();
        this.#displaying = false;
    }
    
    /** Display's the list of suggestions gotten from backend. */
    async display(user_input) {
        this.the_hints = await this.__get_backend_hints(user_input);
        // console.log(this.the_hints);

        if (this.the_hints.length){
            this.selected_hint = 0;
            this.renderer.render_hints(this.the_hints, this.selected_hint);
            this.#displaying = true;
            return;
        }

        this.hide();
    }
    
    move_hint_selection(direction) {
        let hints_len = this.the_hints.length

        switch (direction) {
            case "up":
                if (this.selected_hint > 0){
                    this.selected_hint -= 1;
                }
                break;
            
            case "down":
                if (this.selected_hint < (hints_len-1)){
                    this.selected_hint += 1;
                }
                break;
    
            default:
        }

        this.renderer.update_hints(this.the_hints, this.selected_hint);
    }
}