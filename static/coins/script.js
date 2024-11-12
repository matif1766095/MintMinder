function addCoin(event) {
    event.preventDefault();
    const coinData = {
        name: document.getElementById('addName').value,
        type: document.getElementById('addType').value,
        value: parseFloat(document.getElementById('addValue').value),
        quantity: parseInt(document.getElementById('addQuantity').value),
        description: document.getElementById('addDescription').value,
    };

    fetch('/coins', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(coinData),
    })
        .then(response => {
            if (response.ok) {
                alert('Coin added successfully!');
                window.location.reload();
            } else {
                alert('Failed to add coin.');
            }
        });
}

function saveCoin() {
    const coinId = document.getElementById('editCoinId').value;
    const coinData = {
        name: document.getElementById('editName').value,
        type: document.getElementById('editType').value,
        value: parseFloat(document.getElementById('editValue').value),
        quantity: parseInt(document.getElementById('editQuantity').value),
        description: document.getElementById('editDescription').value,
    };

    console.log("Saving coin data:", coinData);

    fetch(`/coins/${coinId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(coinData),
    })
        .then(response => {
            if (response.ok) {
                alert('Coin updated successfully!');
                window.location.reload();
            } else {
                alert('Failed to update coin.');
            }
        });

    closeEditModal();
}

function openEditModal(coin) {
    console.log("Opening edit modal for coin:", coin);
    document.getElementById('editCoinId').value = coin.id;
    document.getElementById('editName').value = coin.name;
    document.getElementById('editType').value = coin.type;
    document.getElementById('editValue').value = coin.value;
    document.getElementById('editQuantity').value = coin.quantity;
    document.getElementById('editDescription').value = coin.description;
    document.getElementById('editModal').style.display = 'flex';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

function confirmDelete(coinId, coinName) {
    if (confirm(`Are you sure you want to delete ${coinName}?`)) {
        fetch(`/coins/${coinId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (response.ok) {
                    alert('Coin deleted successfully!');
                    window.location.reload();
                } else {
                    alert('Failed to delete coin.');
                }
            });
    }
}
function searchCoins() {
    const search = document.getElementById('search').value.trim();
    const type = document.getElementById('type').value;
    const sort = document.getElementById('sort').value;
    const queryParams = new URLSearchParams();
    if (search) {
        queryParams.append('search', search);
    }
    if (type) {
        queryParams.append('type', type);
    }
    if (sort) {
        queryParams.append('sort', sort);
    }
    window.location.href = `/coins?${queryParams.toString()}`;
}

