# Django Project

This is a simple Django project that includes two apps: `store` and `order`.
   
## Run the Development Server
   
```python manage.py runserver```

## Admin Authentication
```
  email: lizi@abc.com
  password: unchainedd
```
## Access the Application
The default configuration is localhost:8000. Replace with your server/port.
- Admin Interface: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

### Language Support
The project has i18n support for English (default) and Georgian languages.
Use the url prefix `/ka` to change the language setting to Georgian.

### Pages Using Templates
- Store Homepage: [http://127.0.0.1:8000/store](http://127.0.0.1:8000/store)
- Listing Page: [http://127.0.0.1:8000/store/category/](http://127.0.0.1:8000/store/category/)
- Product Detail: [http://127.0.0.1:8000/store/product/<slug:slug>](http://127.0.0.1:8000/store/product/any)
- Cart: [http://127.0.0.1:8000/order/cart](http://127.0.0.1:8000/order/cart)
- Checkout: [http://127.0.0.1:8000/order/checkout](http://127.0.0.1:8000/order/checkout)
- Contact: [http://127.0.0.1:8000/store/contact](http://127.0.0.1:8000/store/contact)
- Register: [http://127.0.0.1:8000/user/register](http://127.0.0.1:8000/user/register)
- Login: [http://127.0.0.1:8000/user/login](http://127.0.0.1:8000/user/login)
## Basic Structure / Files Edited
- `myproject/`: Main project directory.
  - `settings.py`: Project settings.
  - `urls.py`: URL configuration.
- `store/`: Store app for managing products and categories.
  - `views.py`: Views for displaying product information.
  - `urls.py`: URL configuration for the store app.
  - `models.py`: Models to manage data for the store app.
  - `admin.py`: Custom ModelAdmin classes.
- `order/`: Order app for managing customer orders.
  - `views.py`: Views for displaying order information.
  - `urls.py`: URL configuration for the order app.
- `user/`: User app for managing custom users. 
  - `models.py`: Custom user models.
  - `admin.py`: Custom ModelAdmin class.