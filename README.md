# Django E-Commerce Project

An advanced and modern e-commerce web application built using Django. This project includes features like product management, user authentication, a shopping cart, and more. It's designed to be responsive and scalable for real-world use.

---

## **Features**
- **User Features:**
  - User authentication (register, login, logout).
  - Add products to favorites.
  - Shopping cart functionality.
  - Search and filter products.
  - Responsive design for mobile, tablet, and desktop.
  - Webscraping implementation.

- **Admin Features:**
  - Add, edit, or delete products.
  - Manage user accounts.
  - Dashboard for managing categories, brands, and more.

---

## **Technologies Used**
- **Backend:** Django 5.1.4
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default) – can be replaced with PostgreSQL
- **Others:**
  - [Python Decouple](https://pypi.org/project/python-decouple/): For environment variable management.
  - [Pillow](https://python-pillow.org/): For image processing.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/ecommerce.git
cd ecommerce
```

### **2. Set Up the Environment**
1. Create a `.env` file in the root directory:
    ```plaintext
    SECRET_KEY=your_secret_key
    DEBUG=False
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

2. Configure your database (optional) in the `.env` file:
    ```plaintext
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_PORT=your_database_port
    ```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Apply Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Run the Development Server**
```bash
python manage.py runserver
```
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the application in action.

---

## **Usage**
1. **Frontend:**
   - Visit the homepage to browse products.
   - Use the search bar or filters to narrow your choices.
   - Add products to your cart or favorites for later.

2. **Admin Panel:**
   - Visit `/admin` to log in to the admin panel.
   - Manage products, categories, users, and more.

---

## **Folder Structure**
```
ecommerce/
├── store/
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── templates/
│   │   └── store/
│   ├── urls.py
│   ├── views.py
│   └── ...
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── static/
├── media/
└── requirements.txt
```

---

## **Contributing**
Contributions are welcome! Here’s how you can contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## **Contact**
For any inquiries or support, please reach out:
- **GitHub:** https://github.com/Ordnarycoder

---

## **Future Improvements**
- Add payment gateway integration (e.g., Stripe, PayPal).
- Enhance the admin dashboard with analytics.
- Implement order tracking.

