# Blog-It - Django Blog Application

A modern, feature-rich blog application built with Django, allowing users to create, share, and engage with content seamlessly. It includes user authentication, post management, a commenting system, tagging, search, and is designed for easy deployment on Render.

## Features

*   **User Authentication**: Secure user registration, login, logout, and password reset functionality.
*   **User Profiles**: Customizable user profiles with profile pictures, bios, and social media links (`Twitter`, `LinkedIn`, `GitHub`).
*   **Post Management (CRUD)**: Users can create, read, update, and delete their blog posts.
*   **Rich Text Editor**: WYSIWYG editor (Summernote) for creating and editing blog posts with formatting options.
*   **Commenting System**: Users can comment on posts, and reply to existing comments.
*   **Tagging**: Posts can be categorized using tags, with a dedicated page to view all posts for a specific tag.
*   **Popular Tags**: Displays a list of popular tags.
*   **Search Functionality**: Users can search for blog posts.
*   **Pagination**: Efficiently handles lists of posts.
*   **Responsive Design**: Built with Bootstrap 5 for a seamless experience across devices.
*   **Static File Serving**: Optimized for production using WhiteNoise.
*   **Admin Interface**: Django admin panel for site administration.
*   **Customizable Site URL/Domain**: Dynamically sets site URL based on environment (development/production).

## Tech Stack

*   **Backend**: Python, Django
*   **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
*   **Database**: PostgreSQL (Production - Render), SQLite (Local Development)
*   **WSGI Server**: Gunicorn (Production)
*   **Static Files**: WhiteNoise (Production)
*   **Editor**: Django Summernote
*   **Forms**: Django Crispy Forms with Bootstrap 5 pack

## Project Structure

```
DJANGO_PROJECT/
├── blog/                 # Core blogging application (models, views, templates for posts, comments, tags)
├── users/                # User management application (models, views, templates for profiles, auth)
├── DJANGO_PROJECT/       # Main project configuration (settings, main URLs, WSGI)
├── templates/            # Global templates (e.g., base layout if not app-specific)
├── static/               # Global static files (CSS, JS, images)
├── media/                # User-uploaded files (e.g., profile pictures)
├── manage.py             # Django's command-line utility
├── requirements.txt      # Python package dependencies
├── runtime.txt           # Python version for Render
├── Procfile              # Defines process types for Heroku/Render (Gunicorn)
├── build.sh              # Build script for Render (installs dependencies, collects static, migrates DB)
├── render.yaml           # Infrastructure-as-Code for Render deployment
└── README.md             # This file
```

## Prerequisites for Local Development

*   Python (version as specified in `runtime.txt`, e.g., 3.13.1)
*   `pip` (Python package installer)
*   Git for version control

## Local Development Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Viverun/BLOG-V01.git
    cd BLOG-V01 # Or your project's root directory name
    ```

2.  **Create and activate a virtual environment**:
    *   On Windows (PowerShell):
        ```powershell
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables (Optional for basic local run, required for email features)**:
    Create a `.env` file in the root project directory (alongside `manage.py`) and add the following (example):
    ```env
    DJANGO_SECRET_KEY='your_very_secret_django_key_here'
    DJANGO_DEBUG=True
    EMAIL_HOST_USER='your_gmail_username@gmail.com'
    EMAIL_HOST_PASSWORD='your_gmail_app_password'
    # DATABASE_URL='sqlite:///db.sqlite3' # Default, not strictly needed in .env for local SQLite
    ```
    *   `DJANGO_SECRET_KEY`: A strong, unique key. The `settings.py` has a default insecure key for development if this is not set.
    *   `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`: For password reset emails via Gmail. Generate an "App Password" for `EMAIL_HOST_PASSWORD` if using 2FA with Gmail.

5.  **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser** (for admin panel access):
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email, and password.

7.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```

8.  Open your browser and navigate to `http://127.0.0.1:8000/`.

## Environment Variables (Production)

The following environment variables need to be configured in your production environment (e.g., on Render):

*   `DJANGO_SECRET_KEY`: **Required**. A strong, unique secret key.
*   `DJANGO_DEBUG`: **Required**. Set to `False`.
*   `DJANGO_ALLOWED_HOST`: **Required**. Your production domain(s) (e.g., `your-app-name.onrender.com,www.yourdomain.com`).
*   `DATABASE_URL`: **Required**. Provided by your Render PostgreSQL service (automatically injected if using `render.yaml`).
*   `PYTHON_VERSION`: Specified in `runtime.txt` and `render.yaml`.
*   `EMAIL_HOST_USER`: (Optional) Your Gmail address for sending emails.
*   `EMAIL_HOST_PASSWORD`: (Optional) Your Gmail app password.
*   `WEB_CONCURRENCY`: (Optional) Number of Gunicorn workers. Render sets a default.

## Running Tests

To run the automated tests for the application:
```bash
python manage.py test
```
This will discover and run tests in the `blog` and `users` applications.

## Deploying to Render (Free Tier)

This project is configured for deployment on Render's free tier using the provided `render.yaml` (Blueprint) and `build.sh` script.

### Prerequisites for Render Deployment:
1.  **Render Account**: Sign up at [render.com](https://render.com/).
2.  **GitHub Repository**: Your project code pushed to a GitHub repository. Render will connect to this.

### Deployment Options:

**Option 1: Using Render Blueprint (`render.yaml` - Recommended)**

1.  **Commit `render.yaml`**: Ensure the `render.yaml` file in your repository is up-to-date and correctly configured. This file defines your services (web server and database) and environment settings.
2.  **Create New Blueprint Instance on Render**:
    *   Go to your Render Dashboard.
    *   Click "New" -> "Blueprint".
    *   Connect your GitHub account and select the repository for your Django project.
    *   Render will automatically detect and parse the `render.yaml` file.
    *   Review the services and environment variables.
        *   The `DJANGO_SECRET_KEY` will be generated automatically by Render as specified in `render.yaml` (`generateValue: true`). You can also set it manually if preferred.
        *   The `DATABASE_URL` will be automatically provided by the Render PostgreSQL service and injected into your web service's environment.
    *   Click "Create Blueprint Instance" (or "Apply" if updating).
3.  **Deployment**: Render will build and deploy your application based on `render.yaml` and `build.sh`.
4.  **Set Custom Domain (Optional)**: Once deployed, you can add a custom domain in your Render service settings.

**Option 2: Manual Setup on Render Dashboard**

If you prefer not to use a Blueprint or need more granular control during setup:

1.  **Create a PostgreSQL Database on Render**:
    *   Go to your Render Dashboard.
    *   Click "New" -> "PostgreSQL".
    *   Choose a name, region, and plan (free tier available).
    *   Once created, Render will provide a `DATABASE_URL` (Internal Connection String). Copy this.

2.  **Create a Web Service on Render**:
    *   Go to your Render Dashboard.
    *   Click "New" -> "Web Service".
    *   Connect your GitHub account and select the repository.
    *   Configure the service:
        *   **Name**: Choose a name for your web service (e.g., `my-django-app`).
        *   **Region**: Choose a region.
        *   **Branch**: Select the branch to deploy (e.g., `main` or `master`).
        *   **Root Directory**: Leave blank if your `manage.py` is at the root.
        *   **Runtime**: Select `Python`.
        *   **Build Command**: `./build.sh`
        *   **Start Command**: `gunicorn DJANGO_PROJECT.wsgi:application` (as defined in your `Procfile`).
        *   **Instance Type**: Choose the free tier.
    *   **Environment Variables**:
        *   Click "Advanced" or "Environment" section.
        *   Add `DATABASE_URL` and paste the internal connection string from your Render PostgreSQL service.
        *   Add `PYTHON_VERSION` (e.g., `3.13.1` - matching your `runtime.txt`).
        *   Add `DJANGO_SECRET_KEY` (generate a strong unique key).
        *   Add `DJANGO_DEBUG` and set it to `False`.
        *   Add `DJANGO_ALLOWED_HOST` (e.g., `your-app-name.onrender.com`).
        *   (Optional) `WEB_CONCURRENCY`: Render's default is usually fine for the free tier.
    *   Click "Create Web Service".

3.  **Deployment**: Render will pull your code, run the build command, and then the start command.

### First-Time Setup Commands (After Initial Deployment on Render)

Render's `build.sh` handles migrations (`python manage.py migrate`). However, you will likely need to create a superuser manually for the first time if not scripted:

1.  **Open Render Shell**: Go to your Web Service on Render and open the "Shell" tab.
2.  **Create Superuser**: Run the following command:
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin user.

### Local Testing of Production-like Setup (Simulating Render)

Before pushing, or to debug, you can simulate parts of the production environment locally.

1.  **Ensure `deploy_render.ps1` (if used) or manual steps are clear.**
    The `deploy_render.ps1` script can help automate checks and local testing steps.

2.  **To fully simulate, set environment variables locally (e.g., in your shell or a `.env` file loaded by a tool like `python-dotenv` if you integrate it):**
    *   `DJANGO_SECRET_KEY='a_strong_production_key'`
    *   `DJANGO_DEBUG=False`
    *   `DATABASE_URL='your_local_postgresql_connection_string'` (if testing with PostgreSQL locally)
    *   `DJANGO_ALLOWED_HOST='localhost,127.0.0.1'`

    Then run the build and start commands (ensure `psycopg2-binary` is in `requirements.txt` for PostgreSQL):
    ```bash
    # On Linux/macOS or Git Bash/WSL on Windows
    ./build.sh
    gunicorn DJANGO_PROJECT.wsgi:application

    # Or, manually execute build steps if ./build.sh is problematic on native Windows:
    # pip install -r requirements.txt
    # python manage.py collectstatic --noinput --clear
    # python manage.py migrate
    # gunicorn DJANGO_PROJECT.wsgi:application
    ```

### Important Notes for Render:
*   **Free Tier Limitations**: Render's free tier services may spin down after a period of inactivity, leading to a delay on the first request after a while. PostgreSQL on the free tier has limited storage and connections.
*   **Static Files**: `WhiteNoise` is configured to serve static files. `build.sh` runs `collectstatic`.
*   **Database Migrations**: `build.sh` runs `migrate`.
*   **Logging**: Check your application logs in the Render dashboard for any deployment or runtime errors.
*   **`runtime.txt`**: Specifies the Python version for Render to use.
*   **`Procfile`**: Defines the `web` process type. Render uses the "Start Command" from the dashboard, which should match the `Procfile`.
*   **`build.sh`**: Crucial script for preparing the application. Ensure it's executable (Git handles this: `git add --chmod=+x build.sh`).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details (if one exists, otherwise, you may consider adding one).