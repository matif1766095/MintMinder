# Game Coin Management System

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Routes](#routes)
- [Models](#models)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Overview
The **Game Coin Management System** is a web application built using Flask and SQLite to allow users to manage their virtual game currencies. Users can register, log in, add, update, delete, and view their game coins, along with tracking their transaction history. The application also supports importing and exporting coin data in CSV format, making it easy to manage large inventories.

## Features
- User registration and authentication
- Add, update, and delete game coins
- Search and filter functionality for coins
- Transaction history tracking
- Import and export game coins using CSV files
- Reporting on total value and quantity of game coins
- User-friendly interface

## Technologies Used
- **Flask**: A micro web framework for Python
- **Flask-SQLAlchemy**: An extension for Flask that adds SQLAlchemy support
- **Flask-Login**: User session management for Flask
- **SQLite**: A lightweight database engine
- **HTML/CSS**: For front-end development
- **Bootstrap**: For responsive design
- **Pandas**: For data manipulation when importing CSV files
- **Werkzeug**: For secure password hashing

## Installation

To get started with the Game Coin Management System, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/game-coin-management-system.git
   cd game-coin-management-system
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database:**
   The database will be automatically created when you run the application for the first time. However, you can also manually create it using:
   ```python
   from app import db
   db.create_all()
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```

7. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage
1. **Registration:** Navigate to the `/register` route to create a new user account.
2. **Login:** Use the `/login` route to authenticate your account.
3. **Manage Coins:** After logging in, you can manage your game coins through the `/coins` route, where you can add, update, and delete coins.
4. **Transaction History:** View your transaction history at the `/transactions` route.
5. **Import/Export Coins:** You can import game coins via CSV files at the `/import` route and export your coins as CSV at the `/export` route.
6. **Reports:** Access the `/report` route to view insights about your coins.

## Routes
| Route                  | Method | Description                                        |
|------------------------|--------|----------------------------------------------------|
| `/`                    | GET    | Home page                                         |
| `/register`            | GET, POST | User registration page                         |
| `/login`               | GET, POST | User login page                                 |
| `/logout`              | GET    | Log out the user                                 |
| `/profile`             | GET    | User profile page                                |
| `/coins`               | GET, POST | Manage game coins (view/add)                  |
| `/coins/<int:coin_id>` | PUT, DELETE | Modify a specific coin                        |
| `/export`              | GET    | Export coins as CSV                              |
| `/import`              | POST   | Import coins from CSV                            |
| `/transactions`        | GET    | View transaction history                          |
| `/report`              | GET    | View report on game coins                        |

## Models
### User
- `id`: Integer, Primary Key
- `username`: String, Unique
- `email`: String, Unique
- `password`: String
- `transactions`: Relationship to `TransactionHistory`

### GameCoin
- `id`: Integer, Primary Key
- `name`: String
- `type`: String
- `value`: Float
- `quantity`: Integer
- `description`: Text
- `date_added`: DateTime

### TransactionHistory
- `id`: Integer, Primary Key
- `user_id`: Integer, Foreign Key
- `action`: String
- `timestamp`: DateTime

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add your message'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to [Flask](https://flask.palletsprojects.com/) and its community for the incredible framework.
- Inspiration from various online resources and documentation.

```

---

## 💬 Contact

Created by **Muhammad Atif** – [Email Me](mailto:muhammad.atif17660@gmail.com)

---
