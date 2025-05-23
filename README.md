
# Blog-IT-V-02

**Blog-IT** is a personal blogging platform built with Django. It allows users to create, edit, and manage blog posts through a user-friendly interface. The application features category and tag management, search functionality, and a responsive design for optimal viewing on various devices.

## ✨ Features

* Create, update, and delete blog posts
* Organize posts using categories and tags
* Search functionality to find posts quickly
* Auto-generated timestamps for posts
* Responsive frontend design using Bootstrap
* SEO-friendly URLs for better search engine visibility([GitHub][1])

## 🛠 Tech Stack

* **Backend:** Django 4.x
* **Database:** SQLite (default), easily swappable with PostgreSQL
* **Frontend:** HTML/CSS with Bootstrap

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Viverun/Blog-IT-V-02.git
   cd Blog-IT-V-02
   ```



2. **Create and activate a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```



3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```



4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```



5. **Create a superuser (for admin access):**

   ```bash
   python manage.py createsuperuser
   ```



6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```



Access the application at `http://127.0.0.1:8000/`

## 📁 Project Structure

```plaintext
Blog-IT-V-02/
├── DJANGO_PROJECT/           # Main Django project directory
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # URL configurations
│   └── wsgi.py
├── .env.example              # Example environment variables file
├── .gitignore
├── Procfile                  # For deployment (e.g., Heroku)
├── README.md
├── build.sh                  # Build script
├── render.yaml               # Deployment configuration for Render
├── requirements.txt          # Python dependencies
└── manage.py                 # Django's command-line utility
```



## 📄 Deployment

The project includes configuration files for deployment on platforms like Render and Heroku.

* **Render:** Utilize `render.yaml` for setting up the service.
* **Heroku:** The `Procfile` is configured for Heroku deployment.

Ensure to set up the necessary environment variables and configurations as per the chosen platform's requirements.

## 📚 Documentation

* Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
* Bootstrap Documentation: [https://getbootstrap.com/docs/](https://getbootstrap.com/docs/)


## 📄 License

This project is licensed under the MIT License.

---

For more details, visit the [Blog-IT-V-02 GitHub repository](https://github.com/Viverun/Blog-IT-V-02/).

---

[1]: https://github.com/pacificrm/BlogLiteV2?utm_source=chatgpt.com "pacificrm/BlogLiteV2: BlogLite is a social blogging web ... - GitHub"
