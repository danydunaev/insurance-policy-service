// ============================================================
// ВОПРОС ТАБЛИЦЫ №22 (оценивание): Диагностика JS
// Подключение: <script src="{% static 'homepage/js/main.js' %}"></script>
// Элемент: <span id="current-year"></span>
// Если файл не загрузился — в DevTools → Network будет 404.
// Если файл загрузился, но есть ошибка — в Console будет сообщение.
// ============================================================

const yearElement = document.getElementById('current-year');
if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}