/** 
 * @file frontend/site/scripts/easter_eggs.js
 * 
 * @version 0.1
 */

export function showMilvusDialog() {
  	const modal = document.createElement("dialog");
  	modal.className = "milvus-dialog";
  	modal.innerHTML = `
    	<p>I &#128151 Milvus</p>
    	<button class="closeDialog milvus" aria-label="Fechar">&times;</button>
  	`;
  	document.body.appendChild(modal);

  	modal.querySelector(".closeDialog.milvus").addEventListener("click", () => {
    	modal.remove(); // destroy when closed
  	});
}

export function showPokemonDialog() {
  	const modal = document.createElement("dialog");
  	modal.className = "pokemon-dialog";
  	modal.innerHTML = `
    	<a href="https://youtu.be/L9gl6yBA7wU?si=Q47KV7mFLSi6gqju" target="_blank"> 
			<img src="https://pt.quizur.com/_image?href=https%3A%2F%2Fimg.quizur.com%2Ff%2Fimg5f7340bb214684.72884410.png%3FlastEdited%3D1601388742&w=600&h=600&f=webp" 
			alt="Monképo"></a>
    	<button class="closeDialog milvus" aria-label="Fechar">&times;</button>
  	`;
  	document.body.appendChild(modal);

  	modal.querySelector(".closeDialog.milvus").addEventListener("click", () => {
    	modal.remove(); // destroy when closed
  	});
}