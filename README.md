# CodeAlpha EbenKart 

Welcome to **CodeAlpha EbenKart**, a robust, database-driven e-commerce backend built with Python and Django. This project provides a structured database schema and admin interface to manage a catalog of products, user shopping carts, and completed orders.

---

## Features

### 📦 1. Catalog Management (`catalog` app)
* **Product Model:** Fields for name, description, price, stock quantity, image URLs, and auto-timestamps.
* **Admin Customization:** Register products in the admin panel for quick creation, deletion, and searching.

### 2. Shopping Cart & Order Tracking (`cart` app)
* **Active Cart (`Cart`, `CartItem`):** Tracks current active shopping sessions, linked uniquely per Django user.
* **Order History (`Order`, `OrderItem`):** Saves permanent records of finalized checkouts. If a product is removed from the active catalog, historical order details persist without crashing.

###  3. Admin Control Panel
* Pre-configured Django administration dashboards for easy management of products, customer carts, and orders.

---

## Project Structure

```text
CodeAlpha_EbenKart/
│
├── catalog/                # Catalog App (Products, Inventory)
│   ├── migrations/         # Database migrations
│   ├── admin.py            # Product admin interface registration
│   └── models.py           # Product database schema
│
├── cart/                   # Cart App (Carts, Items, Orders)
│   ├── migrations/         # Database migrations
│   ├── admin.py            # Cart & Order admin registrations
│   └── models.py           # Cart, CartItem, Order, & OrderItem models
│
├── store_project/          # Main Project Configuration
│   ├── settings.py         # App configuration & database settings
│   ├── urls.py             # URL router configuration
│   └── wsgi.py / asgi.py   # Web server gateways
│
├── db.sqlite3              # SQLite Database file
├── manage.py               # Django management CLI utility
└── requirements.txt        # Project dependencies
```

---

## Installation & Setup Guide

Follow these steps to set up and run CodeAlpha EbenKart on your local environment:

### Prerequisites
* **Python 3.10+** installed on your system.
* **pip** (Python package installer).

---

### Step-by-Step Installation

#### 1. Navigate to the Project Directory
Open your terminal or command prompt and change directory to the project folder:
```bash
cd "CodeAlpha_EbenKart"
```

#### 2. Set Up a Virtual Environment (Optional but Recommended)
Create a new Python virtual environment named `venv`:
```bash
python -m venv venv
```

Activate the virtual environment:
* **On Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **On Windows (Command Prompt):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```
* **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

#### 3. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

#### 4. Run Database Migrations
Create and configure the database tables:
```bash
python manage.py migrate
```

#### 5. Create a Superuser / Admin Account
To access the e-commerce dashboard backend, generate an administrative user account:
```bash
python manage.py createsuperuser
```
Follow the interactive prompts to define your admin **username**, **email address**, and **password**.

#### 6. Start the Development Server
Launch Django's local development server:
```bash
python manage.py runserver
```

---

##  How to Use

1. Once the server is running, open your web browser and go to:
   [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
2. Log in using the **Superuser credentials** you created in Step 5.
3. From the dashboard:
   * Add new e-commerce **Products** under the Catalog section.
   * View and manage user **Carts** and **Cart Items**.
   * Track, edit, or finalize client **Orders** and **Order Items**.

---

##  Tech Stack
* **Language:** Python
* **Framework:** Django 6.0.5
* **Database:** SQLite (default development database)