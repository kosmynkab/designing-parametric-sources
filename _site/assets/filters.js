const cards = [...document.querySelectorAll(".specimen-card")];
const axisGroupFilter = document.querySelector("#axis-group-filter");
const glyphGroupFilter = document.querySelector("#glyph-group-filter");
const styleFilter = document.querySelector("#style-filter");
const axisFilter = document.querySelector("#axis-filter");
const groupOrder = ["uppercase", "lowercase", "figures", "punctuation", "symbols", "parts",];

const specimenGrid = document.querySelector(".specimen-grid");

cards.sort((firstCard, secondCard) => {
  const firstGroup = groupOrder.indexOf(firstCard.dataset.group);
  const secondGroup = groupOrder.indexOf(secondCard.dataset.group);

  if (firstGroup !== secondGroup) {
    return firstGroup - secondGroup;
  }

  const glyphOrder = firstCard.dataset.glyph.localeCompare(
    secondCard.dataset.glyph
  );

  if (glyphOrder !== 0) {
    return glyphOrder;
  }

  return firstCard.dataset.axis.localeCompare(secondCard.dataset.axis);
});

for (const card of cards) {
  specimenGrid.append(card);
}

const axisGroups = [...new Set(
  cards.map(card => card.dataset.axisGroup)
)]
  .filter(Boolean)
  .sort();

for (const axisGroup of axisGroups) {
  const option = document.createElement("option");
  option.value = axisGroup;
  option.textContent = axisGroup;
  axisGroupFilter.append(option);
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

const axes = [...new Set(
  cards.map(card => card.dataset.axis)
)]
  .filter(Boolean)
  .sort();

for (const axis of axes) {
  const option = document.createElement("option");
  option.value = axis;
  option.textContent = axis;
  axisFilter.append(option);
}

function updateCards() {
  const selectedAxisGroup = axisGroupFilter.value;
  const selectedGlyphGroup = glyphGroupFilter.value;
  const selectedStyle = styleFilter.value;
  const selectedAxis = axisFilter.value;

  for (const card of cards) {
    const matchesAxisGroup = (
      !selectedAxisGroup ||
      card.dataset.axisGroup === selectedAxisGroup
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

    card.hidden = !(matchesAxisGroup && matchesGlyphGroup && matchesStyle && matchesAxis);
  }
}

axisGroupFilter.addEventListener("change", updateCards);
glyphGroupFilter.addEventListener("change", updateCards);
styleFilter.addEventListener("change", updateCards);
axisFilter.addEventListener("change", updateCards);