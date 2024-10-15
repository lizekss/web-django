# Django Project

This is a simple Django project that includes two apps: `store` and `order`.
   
## Run the Development Server
   
```python manage.py runserver```

## Admin Authentication
```
  user: lizekss
  password: unchainedddd
```
   
## Access the Application

The default configuration is localhost:8000. Replace with your server/port.
   - Admin Interface: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
   - Store App: [http://127.0.0.1:8000/store/products/](http://127.0.0.1:8000/store/products/)
   - Order App: [http://127.0.0.1:8000/order/orders/](http://127.0.0.1:8000/order/orders/)
   - Categories: [http://127.0.0.1:8000/store/category/](http://127.0.0.1:8000/store/categories/)

## Basic Structure / Files Edited
- `myproject/`: Main project directory.
  - `settings.py`: Project settings.
  - `urls.py`: URL configuration.
- `store/`: Store app for managing products and categories.
  - `views.py`: Views for displaying product information.
  - `urls.py`: URL configuration for the store app.
  - `models.py`: Models to manage data for the store app.
- `order/`: Order app for managing customer orders.
  - `views.py`: Views for displaying order information.
  - `urls.py`: URL configuration for the order app.
