const specimenZoomButtons = document.querySelectorAll(".specimen-zoom");

if (specimenZoomButtons.length) {
  const imageDialog = document.createElement("dialog");

  imageDialog.className = "image-dialog";
  imageDialog.innerHTML = `
    <div class="image-dialog__content">
      <button
        class="image-dialog__close"
        type="button"
        aria-label="Close enlarged image"
      >
        x
      </button>

      <figure class="image-dialog__figure">
        <div class="image-dialog__proof"></div>
        <figcaption class="image-dialog__caption"></figcaption>
      </figure>
    </div>
  `;

  document.body.append(imageDialog);

  const dialogProof = imageDialog.querySelector(".image-dialog__proof");
  const dialogCaption = imageDialog.querySelector(".image-dialog__caption");
  const closeButton = imageDialog.querySelector(".image-dialog__close");

  specimenZoomButtons.forEach((button) => {
    const image = button.querySelector("img");

    if (image && !button.hasAttribute("aria-label")) {
      button.setAttribute("aria-label", `Enlarge ${image.alt}`);
    }

    button.addEventListener("click", () => {
      const caption = button.closest("figure").querySelector("figcaption");
      const inlineProof = button.querySelector(".proof-viewer__svg");
      const fallbackImage = button.querySelector("img");

      dialogProof.replaceChildren();

      if (inlineProof) {
        const dialogSvg = inlineProof.cloneNode(true);

        dialogSvg.removeAttribute("id");
        dialogSvg.setAttribute("aria-hidden", "true");

        dialogProof.append(dialogSvg);
      } else if (fallbackImage) {
        const dialogImage = document.createElement("img");

        dialogImage.src = fallbackImage.currentSrc || fallbackImage.src;
        dialogImage.alt = fallbackImage.alt;

        dialogProof.append(dialogImage);
      }

      dialogCaption.textContent = caption ? caption.textContent : "";
      imageDialog.showModal();
    });
  });

  closeButton.addEventListener("click", () => imageDialog.close());

  imageDialog.addEventListener("click", (event) => {
    if (event.target === imageDialog) {
      imageDialog.close();
    }
  });
}