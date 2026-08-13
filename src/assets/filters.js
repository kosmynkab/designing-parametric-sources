const cards = [...document.querySelectorAll(".specimen-card")];
const canonicalAxisFilter = document.querySelector("#canonical-axis-filter");
const glyphGroupFilter = document.querySelector("#glyph-group-filter");
const styleFilter = document.querySelector("#style-filter");
const axisFilter = document.querySelector("#axis-filter");
const groupOrder = ["uppercase", "lowercase", "figures", "punctuation", "symbols", "parts",];

const specimenGrid = document.querySelector(".specimen-grid");

cards.sort((firstCard, secondCard) => {
  const firstGroup = groupOrder.indexOf(firstCard.dataset.group);
  const secondGroup = groupOrder.indexOf(secondCard.dataset.group);
  const instanceOrder = {min: 0, max: 1,};

  if (firstGroup !== secondGroup) {return firstGroup - secondGroup;}

  const glyphOrder = firstCard.dataset.glyph.localeCompare(secondCard.dataset.glyph);

  if (glyphOrder !== 0) {return glyphOrder;}
  
  const axisOrder = firstCard.dataset.axis.localeCompare(secondCard.dataset.axis);

if (axisOrder !== 0) {return axisOrder;}

return (
  (instanceOrder[firstCard.dataset.instance] ?? 2) -
  (instanceOrder[secondCard.dataset.instance] ?? 2)
  );
});

for (const card of cards) {
  specimenGrid.append(card);
}

const canonicalAxes = [...new Set(
  cards.map(card => card.dataset.canonicalAxis)
)]
  .filter(Boolean)
  .sort();

for (const canonicalAxis of canonicalAxes) {
  const option = document.createElement("option");
  option.value = canonicalAxis;
  option.textContent = canonicalAxis;
  canonicalAxisFilter.append(option);
}

const glyphGroups = [...new Set(
  cards.map(card => card.dataset.group)
)]
  .filter(Boolean)
  .sort();

for (const glyphGroup of glyphGroups) {
  const option = document.createElement("option");
  option.value = glyphGroup;
  option.textContent = glyphGroup;
  glyphGroupFilter.append(option);
}

const styles = [...new Set(
  cards.map(card => card.dataset.style)
)]
  .filter(Boolean)
  .sort();

for (const style of styles) {
  const option = document.createElement("option");
  option.value = style;
  option.textContent = style[0].toUpperCase() + style.slice(1);
  styleFilter.append(option);
}

function populateAxisFilter() {
  const selectedCanonicalAxis = canonicalAxisFilter.value;

  const axes = [...new Set(
    cards
      .filter(card => (
        !selectedCanonicalAxis ||
        card.dataset.canonicalAxis === selectedCanonicalAxis
      ))
      .map(card => card.dataset.axis)
  )]
    .filter(Boolean)
    .sort();

  axisFilter.replaceChildren(
    new Option("All design axes", "")
  );

  for (const axis of axes) {
    axisFilter.append(
      new Option(axis, axis)
    );
  }

  if (!axes.includes(axisFilter.value)) {
    axisFilter.value = "";
  }
}

populateAxisFilter();

function updateCards() {
  const selectedCanonicalAxis = canonicalAxisFilter.value;
  const selectedGlyphGroup = glyphGroupFilter.value;
  const selectedStyle = styleFilter.value;
  const selectedAxis = axisFilter.value;

  for (const card of cards) {
    const matchesCanonicalAxis = (
      !selectedCanonicalAxis ||
      card.dataset.canonicalAxis === selectedCanonicalAxis
    );

    const matchesGlyphGroup = (
      !selectedGlyphGroup ||
      card.dataset.group === selectedGlyphGroup
    );
    
    const matchesStyle = (
      !selectedStyle ||
      card.dataset.style === selectedStyle
    );

    const matchesAxis = (
      !selectedAxis ||
      card.dataset.axis === selectedAxis
    );

    card.hidden = !(matchesCanonicalAxis && matchesGlyphGroup && matchesStyle && matchesAxis);
  }
}

canonicalAxisFilter.addEventListener("change", () => {
  populateAxisFilter();
  updateCards();
});

glyphGroupFilter.addEventListener("change", updateCards);
styleFilter.addEventListener("change", updateCards);
axisFilter.addEventListener("change", updateCards);