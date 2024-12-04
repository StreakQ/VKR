let deleteItemId;

function showDeleteConfirmationTheme(itemId, theme_name) {
    deleteItemId = itemId;
    const message = `Вы уверены, что хотите удалить Тему?\n\nID: ${itemId}\nФИО: ${theme_name} `;
    document.getElementById('deleteConfirmationMessage').innerText = message;
    document.getElementById('confirmDeleteModal').style.display = 'block';
}

document.getElementById('confirmDeleteButton').onclick = function() {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/delete_theme/${deleteItemId}`;
    document.body.appendChild(form);
    form.submit();
};

document.getElementById('cancelDeleteButton').onclick = function() {
    document.getElementById('confirmDeleteModal').style.display = 'none';
};