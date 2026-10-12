const themeToggle = document.querySelector("[data-theme-toggle]");
const themeStorageKey = "theme";

function setTheme(theme, saveTheme = true) {
  document.documentElement.dataset.theme = theme;

  if (saveTheme) {
    localStorage.setItem(themeStorageKey, theme);
  }

  if (themeToggle) {
    const nextTheme = theme === "dark" ? "light" : "dark";
    themeToggle.textContent =
      theme === "dark" ? "Light mode" : "Dark mode";
    themeToggle.setAttribute(
      "aria-label",
      `Switch to ${nextTheme} mode`
    );
  }
}

if (themeToggle) {
  setTheme(document.documentElement.dataset.theme, false);

  themeToggle.addEventListener("click", () => {
    const currentTheme = document.documentElement.dataset.theme;
    setTheme(currentTheme === "dark" ? "light" : "dark");
  });
}