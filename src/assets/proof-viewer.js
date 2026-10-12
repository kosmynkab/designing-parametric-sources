const proofCache = new Map();

const proofColours = new Map([
  ["rgb(0,0,0)", "var(--proof-ink)"],
  ["rgb(242,242,242)", "var(--proof-glyph)"],
  ["rgb(204,204,204)", "var(--proof-guide)"],
  ["rgb(216,216,216)", "var(--proof-guide)"],
  ["rgb(153,153,153)", "var(--proof-muted)"],
  ["rgb(127,127,127)", "var(--proof-muted)"],
  ["rgb(89,89,89)", "var(--proof-muted)"],
  ["rgb(255,0,0)", "var(--proof-warning)"],
  ["rgb(0,178,0)", "var(--proof-pass)"],
  ["rgb(0,84,255)", "var(--proof-info)"]
]);

async function loadProof(url) {
  if (!proofCache.has(url)) {
    proofCache.set(
      url,
      fetch(url)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Could not load ${url}`);
          }

          return response.text();
        })
    );
  }

  return proofCache.get(url);
}

function prepareProof(markup, alt) {
  const documentFragment = new DOMParser().parseFromString(
    markup,
    "image/svg+xml"
  );

  const svg = documentFragment.documentElement;

  if (svg.nodeName === "parsererror") {
    throw new Error("Invalid SVG");
  }

  svg.querySelectorAll("script, foreignObject").forEach((element) => {
    element.remove();
  });

  svg.querySelectorAll("[fill], [stroke]").forEach((element) => {
    for (const property of ["fill", "stroke"]) {
      const value = element.getAttribute(property);

      if (proofColours.has(value)) {
        element.style.setProperty(property, proofColours.get(value));
      }
    }
  });

  svg.classList.add("proof-viewer__svg");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", alt);
  svg.setAttribute("focusable", "false");

  return svg;
}

async function upgradeProof(viewer) {
  const fallback = viewer.querySelector("img");
  const url = fallback.currentSrc || fallback.src;

  try {
    const markup = await loadProof(url);
    const svg = prepareProof(markup, fallback.alt);

    fallback.replaceWith(svg);
    viewer.dataset.proofLoaded = "true";
  } catch (error) {
    viewer.dataset.proofError = "true";
    console.warn(error);
  }
}

const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) {
        continue;
      }

      observer.unobserve(entry.target);
      upgradeProof(entry.target);
    }
  },
  { rootMargin: "600px 0px" }
);

document.querySelectorAll("[data-proof-viewer]").forEach((viewer) => {
  observer.observe(viewer);
});