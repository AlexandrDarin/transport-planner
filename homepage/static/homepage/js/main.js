// Текущий год в подвале сайта.
const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

// Автофокус на поле поиска, если оно есть на странице.
document.addEventListener("DOMContentLoaded", () => {
    const search = document.querySelector('[data-autofocus="true"]');
    if (search) {
        search.focus();
    }
});
