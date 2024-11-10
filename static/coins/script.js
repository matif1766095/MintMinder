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
