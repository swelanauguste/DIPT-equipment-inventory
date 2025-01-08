# DIPT Equipment Inventory

## Overview
DIPT Equipment Inventory is a web application designed to manage and track inventory of various equipment such as computers, printers, scanners, monitors, and more. This application allows users to add, update, and delete items, as well as record transactions related to the equipment.

## Features
- **Item Management**: Add, update, and delete items in the inventory.
- **Transaction Management**: Record transactions (in/out) for each item.
- **Search and Filter**: Search and filter items based on various criteria such as name, serial number, status, model, and operating system.
- **User Authentication**: Secure login and user management.
- **Responsive Design**: User-friendly interface that works on both desktop and mobile devices.

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default, can be configured to use other databases)
- **Version Control**: Git

## Setup Instructions

### Prerequisites
- Python 3.x
- Git

### Steps to Clone and Setup

1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/DIPT-equipment-inventory.git
    cd DIPT-equipment-inventory
    ```

2. **Create a Virtual Environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply Migrations**
    ```sh
    python manage.py migrate
    ```

5. **Create a Superuser**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the Development Server**
    ```sh
    python manage.py runserver
    ```

7. **Access the Application**
    Open your web browser and go to `http://127.0.0.1:8000/`

### Configuration
- **Database**: The default configuration uses SQLite. To use a different database, update the `DATABASES` setting in `settings.py`.
- **Static Files**: Ensure static files are collected using `python manage.py collectstatic` for production deployment.

### Usage
- **Login**: Use the superuser credentials created during setup to log in.
- **Add Items**: Navigate to the "Add item" section to add new equipment.
- **Manage Transactions**: Record transactions for each item from the item detail view.
- **Search and Filter**: Use the search bar and filters to find specific items.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](http://_vscodecontentref_/1) file for more details.

## Contact
For any questions or suggestions, please contact [your-email@example.com].
