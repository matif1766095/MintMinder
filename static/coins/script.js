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
