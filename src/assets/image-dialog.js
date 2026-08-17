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
        <img class="image-dialog__image" alt="">
        <figcaption class="image-dialog__caption"></figcaption>
      </figure>
    </div>
  `;

  document.body.append(imageDialog);

  const dialogImage = imageDialog.querySelector(".image-dialog__image");
  const dialogCaption = imageDialog.querySelector(".image-dialog__caption");
  const closeButton = imageDialog.querySelector(".image-dialog__close");

  specimenZoomButtons.forEach((button) => {
    const image = button.querySelector("img");

    if (image && !button.hasAttribute("aria-label")) {
      button.setAttribute("aria-label", `Enlarge ${image.alt}`);
    }

    button.addEventListener("click", () => {
      const caption = button.closest("figure").querySelector("figcaption");

      dialogImage.src = image.currentSrc || image.src;
      dialogImage.alt = image.alt;
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