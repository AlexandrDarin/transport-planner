// Небольшое клиентское улучшение: автоматически фокусируем поиск при наличии поля.
document.addEventListener('DOMContentLoaded', () => {
  const search = document.querySelector('[data-autofocus="true"]');
  if (search) search.focus();
});
