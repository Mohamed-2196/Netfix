# Netfix - Home Services Platform

## Description
HomeFix is a web-based platform designed to connect customers with service providers for various home-related tasks. Whether you need to fix a bidet, paint your walls, or clean your house, HomeFix makes it easy to find and request services from trusted companies. The platform is built using Django, a powerful Python web framework, and provides a seamless experience for both customers and service providers.

## Features

### User Types
1. **Customer**:
   - Register with email, password, username, and date of birth.
   - Login using email and password.
   - View and request services.
   - Access a profile page displaying personal information and a history of requested services.

2. **Company**:
   - Register with email, password, username, and field of work.
   - Login using email and password.
   - Create and manage services within their field of work.
   - Access a profile page displaying company information and the services they provide.

### Service Management
- **Service Creation**:
  - Companies can create services with a name, description, field, price per hour, and creation date.
  - The field of work restricts the type of services a company can create, except for "All in One" companies which can create any type of service.

- **Service Display**:
  - A page displaying the most requested services.
  - A page showing all services in reverse creation order (newest first).
  - Category-specific pages displaying services available for each category.

- **Service Details**:
  - Each service has its own page displaying detailed information and the company providing it.
  - Customers can request a service by providing the address and service time (in hours).

### User Profiles
- **Customer Profile**:
  - Displays personal information and a list of previously requested services, including service name, field, cost, request date, and provider company.

- **Company Profile**:
  - Displays company information and a list of services they provide.


## How to Run the Project

### Prerequisites
- Python 3.x
- Django 3.1.14

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mohamed-2196/Netfix.git
   cd NetFix
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser** (Optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Website**:
   Open your browser and go to `http://127.0.0.1:8000/`.

### Project Structure
```
HomeFix/
├── main/                   # Handles common project information
├── services/               # Handles service-related features
├── users/                  # Handles user-related features
├── manage.py               # Django management script
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

### Customization
- **CSS**: You can customize the design by modifying the CSS file located at `netfix/static/css/style.css`.
- **HTML**: Feel free to change the provided HTML templates to suit your design preferences.

## Contributing
Feel free to fork the project and submit pull requests. Any contributions are welcome!

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
