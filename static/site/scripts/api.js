/** 
 * @file frontend/site/scripts/api.js
 * 
 * @author AndreiCristeli
 * @author HexagonalUniverse
 * @author victorxaviercosta
 * 
 * @version 0.2
 */

/** API base IP from where to make backend requests */
const API_BASE = "http://localhost:8000/api";

/** API interface for requesting backend information */
export async function api(endpoint, method = "GET", body = null) {
	const options = {
    	method: method,
    	headers: { "Content-Type": "application/json" },
		credentials: "include"
  	};
  	if (body) {
    	options.body = JSON.stringify(body);
  	}

  	// const res = await fetch(`${API_BASE}${endpoint}`, options);
	const res = await fetch(`api${endpoint}`, options);
	
  	if (!res.ok) {
    	const err = await res.json().catch(() => ({}));
    	throw new Error(err.detail || Error `${res.status}`);
  	}
  	return res.json();
}