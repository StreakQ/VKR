let deleteItemId;

function showDeleteConfirmationDistribution(itemId, studentId, themeId, adviserId) {
    deleteItemId = itemId;
    const message = `Вы уверены, что хотите удалить распределение?\n\nID: ${itemId}\nСтудент: ${studentId}\nТема: ${themeId}\nРуководитель: ${adviserId}`;
    document.getElementById('deleteConfirmationMessage').innerText = message;
    document.getElementById('confirmDeleteModal').style.display = 'block';
}

document.getElementById('confirmDeleteButton').onclick = function() {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/delete_distribution/${deleteItemId}`;
    document.body.appendChild(form);
    form.submit();
};

document.getElementById('cancelDeleteButton').onclick = function() {
    document.getElementById('confirmDeleteModal').style.display = 'none';
};