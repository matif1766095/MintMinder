function confirmLogout(event) {
    if (!confirm("Are you sure you want to log out?")) {
        event.preventDefault(); // Prevent the default logout action
    }
}