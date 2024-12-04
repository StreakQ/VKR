let deleteItemId;

function showDeleteConfirmationAdviser(itemId, firstname,lastname,patronymic) {
    deleteItemId = itemId;
    const message = `Вы уверены, что хотите удалить Научного руководителя?\n\nID: ${itemId}\nФИО: ${firstname}  ${lastname}  ${patronymic}`;
    document.getElementById('deleteConfirmationMessage').innerText = message;
    document.getElementById('confirmDeleteModal').style.display = 'block';
}

document.getElementById('confirmDeleteButton').onclick = function() {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/delete_adviser/${deleteItemId}`;
    document.body.appendChild(form);
    form.submit();
};

document.getElementById('cancelDeleteButton').onclick = function() {
    document.getElementById('confirmDeleteModal').style.display = 'none';
};