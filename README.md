# Title -  Inventory Management System

    This application provides a backend API for managing inventory items using Flask, SQLAlchemy, and SQLite. 
    It also features a frontend built with PyQt5 for a user-friendly interface to interact with the inventory system.
    
## Table of Contents
    1. Tech Stack 
    2. Features
    3. Installation
    4. API Endpoints
    5. Other Info
    6. Documentation

## Tech Stack

    Backend   :Flask ,Flask-Sqalchemy ,Flask-MIgrate
    
    Database  :SQLite (or replace with PostgreSQL/MySQL if desired)
    
    GUI:PyQt5


## Features
    - **Add Item:** Allows you to add new inventory items by providing a name and quantity.
    
    - **Update Quantity:** Update the quantity of an existing item.
    
    - **Buy Item:** Decrease the quantity of an item when it is purchased.
    
    - **Return Item:** Increase the quantity of an item when it is returned.
    
    - **Remove Item:** Remove an item from the inventory.

    - **Fetch Inventory:** View all the inventory items and their quantities.
    
## Installation

    1.Prerequisites :
    
    ```bash
      - Python 3.7+
      - pip (Python package installer)
      - SQLite (or another database you prefer, though the app is configured for SQLite by default)
    ```
    
    2.Clone the repository :
    
       ```bash
       git clone https://github.com/vinodkumarkuruva/Inventory.git
       cd Inventory
       ```
    
    3.Steps to Set Up :
    
    ```bash
    Create a virtual environment          :   python -m venv <name of virtual Environment> 
     	
    To activate the virtual Environment   :   <name of virtual Environment>/Scripts/activate 
     
    Install dependencies                  :   pip install -r requirements.txt
     
    Set up the database                   :   flask db init 
                                              flask db migrate -m "first migration"
                                              flask db upgrade
     
    Run the server                        :   Python app.py  
     
    * The application will start and be accessible at http://127.0.0.1:5000
    
    Run The UI                            :   python ui.py
    
       ```


## Endpoints
- **POST /transform:**  Simulates a transform operation, with a 10-second delay. Expects JSON data.

- **POST /translation:** Simulates a translation operation, with a 10-second delay. Expects JSON data.

- **POST /rotation:** Simulates a rotation operation, with a 10-second delay. Expects JSON data.

- **POST /scale:** Simulates a scale operation, with a 10-second delay. Expects JSON data.

- **GET /file-path:** Retrieves the file path of the project, either as the full path or just the directory.

- **POST /add-item:** Adds a new item to the inventory. Expects name and quantity in JSON format.

- **POST /buy-item:** Buys an item (decreases its quantity). Expects name in JSON format.

- **POST /return-item:** Returns an item (increases its quantity). Expects name in JSON format.

- **POST /remove-item:** Removes an item from the inventory. Expects name in JSON format.

- **POST /update-quantity:** Updates the quantity and max quantity of an item. Expects name and quantity in JSON format.

- **GET /inventory:** Fetches all inventory items, returning their names and quantities in JSON format.

