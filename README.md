# CodeAlpha EbenKart

Welcome to **CodeAlpha EbenKart**, a robust, database-driven e-commerce backend and storefront built with Python and Django. This project provides a complete shopping experience, including a dynamic product catalog, user shopping carts, checkout flow, permanent order tracking, and a comprehensive administration interface.

---

## Features

### 1. Catalog Management (`catalog` app)
* **Product Model:** Detailed schema tracking product names, descriptions, prices, stock quantities, and image URLs.
* **Shop & Details Views:** Dynamic views to list products, view specific categories, and see product details.
* **User Authentication:** Integrated registration and login pages for customers.
* **Admin Customization:** Clean Django Admin panel setup to manage inventory, products, and categories.

### 2. Shopping Cart & Order Tracking (`cart` app)
* **Active Cart (`Cart`, `CartItem`):** Unique, session-persistent shopping carts tied directly to Django users.
* **Checkout & Order History (`Order`, `OrderItem`):** Saves completed checkout sessions as permanent historical records. Even if a product is deleted from the active catalog in the future, order records persist safely (using `models.SET_NULL` on the foreign key relation) without breaking order history.

### 3. Admin Control Panel
* Pre-configured administrative dashboards to manage products, view active carts, and track/update customer orders.

---

## Project Structure

```text
CodeAlpha_EbenKart/
│
├── cart/                       # Cart App (Carts, Items, Orders)
│   ├── migrations/             # Database migrations
│   ├── templates/cart/         # HTML templates (cart_detail.html, order_success.html)
│   ├── admin.py                # Cart & Order admin registrations
│   ├── apps.py                 # App configuration
│   ├── context_processors.py   # Injects cart session details into templates globally
│   ├── models.py               # Cart, CartItem, Order, & OrderItem models
│   ├── urls.py                 # Cart app URL routing
│   └── views.py                # Cart operations, checkout, and order success logic
│
├── catalog/                    # Catalog App (Storefront, Products, Auth)
│   ├── migrations/             # Database migrations
│   ├── static/catalog/         # Static assets (css/, images/)
│   ├── templates/              # HTML templates
│   │   ├── catalog/            # Page templates (base.html, shop.html, product_detail.html, etc.)
│   │   └── registration/       # Auth templates (login.html, register.html)
│   ├── admin.py                # Product admin interface registration
│   ├── apps.py                 # App configuration
│   ├── models.py               # Product database schema (Product model)
│   ├── tests.py                # Unit & integration tests
│   └── views.py                # Frontpage, shop home, category list, contact, and registration views
│
├── store_project/              # Main Project Configuration
│   ├── settings.py             # Global project settings, installed apps, database configuration
│   ├── urls.py                 # Master URL router configuration
│   └── wsgi.py / asgi.py       # Web server gateways
│
├── db.sqlite3                  # SQLite Database file
├── manage.py                   # Django management CLI utility
├── requirements.txt            # Project Python dependencies
└── venv/                       # Python Virtual Environment
```

---

## Installation & Run Guide

> [!IMPORTANT]
> **Directory Context:** All commands must be run from inside the `CodeAlpha_EbenKart` project folder. If you attempt to run python commands from the parent directory, you will receive `can't open file 'manage.py': [Errno 2] No such file or directory`.

Follow these step-by-step instructions to get the application running on your local machine:

### 1. Open Terminal and Navigate to Project Directory
Navigate into the `CodeAlpha_EbenKart` subdirectory:
```bash
cd CodeAlpha_EbenKart
```

### 2. Activate the Virtual Environment
Activate the pre-existing virtual environment (`venv`) to ensure you are using the correct dependencies:
* **On Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **On Windows (Command Prompt / cmd):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```
* **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
Ensure all required Python packages are installed:
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
Set up database tables for the catalog, shopping carts, orders, and built-in auth system:
```bash
python manage.py migrate
```

### 5. Create a Superuser / Admin Account
Create a Django administrative user to log in and populate the database with products:
```bash
python manage.py createsuperuser
```
Follow the prompts in your terminal to specify a **username**, **email address**, and **password**.

### 6. Start the Development Server
Launch the Django server:
```bash
python manage.py runserver
```

Once running successfully, you should see output similar to:
```text
Django version 6.0.5, using settings 'store_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK (or CTRL-C).
```

---

## How to Use

1. **Access the Storefront:**
   Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the homepage.
2. **Access the Shop:**
   Go to [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/) to view the product catalog.
3. **Register/Login:**
   Click **Register** or **Login** on the navigation bar to create a user account and sign in.
4. **Manage Inventory via Admin Dashboard:**
   * Open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with your superuser credentials.
   * Add new **Products** under the **Catalog** section. Give them titles, prices, descriptions, stock quantities, and image URLs.
5. **Interactive Flow:**
   * Browse products on the shop page, select one to view its details, and click **Add to Cart**.
   * Go to the **Cart** page to adjust quantities, remove items, or click **Checkout** to finalize your purchase.
   * View completed orders from the admin panel to track sales and client details.

---

## Tech Stack

* **Language:** Python
* **Framework:** Django 6.0.5
* **Database:** SQLite (local development database)

---

## License & Copyright

&copy; 2026 EbenKart by Ebenezer Papa-Kyi Quayson. All rights reserved. Developed as part of CodeAlpha Projects during my June 2026 internship program.