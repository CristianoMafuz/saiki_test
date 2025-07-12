

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
    <a href="https://monkepo.online/" target="_blank"> <img src="https://monkepo.online/img/monkepo.png" alt="Girl in a jacket"> </a>
    <button class="closeDialog milvus" aria-label="Fechar">&times;</button>
  `;
  document.body.appendChild(modal);

  modal.querySelector(".closeDialog.milvus").addEventListener("click", () => {
    modal.remove(); // destroy when closed
  });
}