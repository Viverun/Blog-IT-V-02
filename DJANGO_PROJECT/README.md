# Blog-It - Django Blog Application

A modern blog application built with Django where users can create, read, update, and delete blog posts. Features include user authentication, comments, and a responsive design.

## Features

- User authentication and profile management
- Create, read, update, and delete blog posts
- Comment system for posts
- Responsive design using Bootstrap
- Rich text editing with Summernote
- Tag system for categorizing posts

## Local Development

### Prerequisites

- Python 3.13+
- pip or uv (package installer)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd DJANGO_PROJECT
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # On Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Visit http://127.0.0.1:8000/ in your browser.

## Deployment to Render

This project is configured for easy deployment on Render's free tier.

### Automatic Deployment

1. Create a [Render account](https://render.com/)
2. Push your code to a GitHub repository
3. In the Render dashboard, click "New" and select "Blueprint"
4. Connect your GitHub repository
5. Render will detect the `render.yaml` configuration automatically
6. Click "Apply" to create and deploy all the necessary services

### Manual Deployment

If you prefer to set up the services manually:

1. In Render, create a new PostgreSQL database (Free tier)
2. Create a new Web Service:
   - Set the build command to: `./build.sh`
   - Set the start command to: `gunicorn DJANGO_PROJECT.wsgi:application`
   - Add the following environment variables:
     - `DATABASE_URL`: (Use the Internal Database URL from your Render PostgreSQL instance)
     - `DJANGO_SECRET_KEY`: (Generate a secure key)
     - `DJANGO_DEBUG`: False
     - `DJANGO_ALLOWED_HOST`: your-app.onrender.com

### First-time Setup After Deployment

After your app is deployed:

1. Open a shell in the Render dashboard 
2. Run these commands to set up your database:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Testing Deployment Locally

To test if your app is ready for deployment:

```
pip install gunicorn dj-database-url whitenoise psycopg2-binary
python manage.py collectstatic
gunicorn DJANGO_PROJECT.wsgi:application
```

## Environment Variables

For production deployment, configure the following environment variables:

- `DJANGO_SECRET_KEY`: A secure secret key
- `DJANGO_DEBUG`: Set to 'False'
- `DJANGO_ALLOWED_HOST`: Your Render domain (e.g., 'blog-app.onrender.com')
- `DATABASE_URL`: PostgreSQL database URL (automatically set by Render)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Deploying to Render (Free Tier)

This project is configured for deployment on Render's free tier.

### Prerequisites:
1.  **Render Account**: Sign up at [render.com](https://render.com/).
2.  **GitHub Repository**: Push your project to a GitHub repository. Render will connect to this repository.
3.  **Environment Variables**: Ensure you have the necessary environment variables ready. Some will be set directly in Render, and `DATABASE_URL` will be provided by Render's PostgreSQL service.
    *   `DJANGO_SECRET_KEY`: A strong, unique secret key. You can generate one using Django's `get_random_secret_key()` or an online generator.
    *   `DJANGO_DEBUG`: Set to `False` for production.
    *   `DJANGO_ALLOWED_HOST`: Your Render app's domain (e.g., `your-app-name.onrender.com`) and any custom domains.
    *   `PYTHON_VERSION`: Specified in `runtime.txt` (e.g., `python-3.13.1`).
    *   `WEB_CONCURRENCY`: (Optional) Number of Gunicorn workers. Render sets a default based on plan.

### Deployment Options:

**Option 1: Using Render Blueprint (render.yaml - Recommended)**

1.  **Commit `render.yaml`**: Ensure the `render.yaml` file in your repository is up-to-date and correctly configured. This file defines your services (web server and database) and environment settings.
2.  **Create New Blueprint Instance on Render**:
    *   Go to your Render Dashboard.
    *   Click "New" -> "Blueprint".
    *   Connect your GitHub account and select the repository for your Django project.
    *   Render will automatically detect and parse the `render.yaml` file.
    *   Review the services and environment variables. You will need to:
        *   Manually add `DJANGO_SECRET_KEY` as a secret environment variable for the web service.
        *   The `DATABASE_URL` will be automatically provided by the Render PostgreSQL service and injected into your web service's environment.
    *   Click "Create Blueprint Instance".
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
        *   **Root Directory**: Leave blank if your `manage.py` is at the root, otherwise specify the path.
        *   **Runtime**: Select `Python`.
        *   **Build Command**: `./build.sh` (or `sh build.sh` if you encounter issues, though `./build.sh` should work given execute permissions are set by git).
        *   **Start Command**: `gunicorn DJANGO_PROJECT.wsgi:application` (as defined in your `Procfile`).
        *   **Instance Type**: Choose the free tier.
    *   **Environment Variables**:
        *   Click "Advanced" or "Environment" section.
        *   Add `DATABASE_URL` and paste the internal connection string from your Render PostgreSQL service.
        *   Add `PYTHON_VERSION` (e.g., `3.13.1` - matching your `runtime.txt`).
        *   Add `DJANGO_SECRET_KEY` (generate a strong unique key).
        *   Add `DJANGO_DEBUG` and set it to `False`.
        *   Add `DJANGO_ALLOWED_HOST` (e.g., `your-app-name.onrender.com`). You can add more later, like your custom domain.
        *   (Optional) `WEB_CONCURRENCY`: Render's default is usually fine for the free tier.
    *   Click "Create Web Service".

3.  **Deployment**: Render will pull your code, run the build command, and then the start command.

### First-Time Setup Commands (After Initial Deployment)

Render's `build.sh` handles migrations (`python manage.py migrate`). However, you might need to create a superuser manually for the first time if not scripted:

1.  **Open Render Shell**: Go to your Web Service on Render and open the "Shell" tab.
2.  **Create Superuser**: Run the following command:
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin user.

### Local Testing of Production Setup (Simulating Render)

Before pushing, or to debug, you can simulate the production environment locally using the `deploy_render.ps1` script or by manually setting environment variables and running the build/start commands.

1.  **Ensure `deploy_render.ps1` is up-to-date.** This script can help:
    *   Check for required files (`requirements.txt`, `runtime.txt`, `Procfile`, `build.sh`).
    *   Install deployment packages (`gunicorn`, `psycopg2-binary`, `dj-database-url`, `whitenoise`) if not already in your local environment (useful for testing `build.sh` steps).
    *   Test static file collection: `python manage.py collectstatic --noinput`
    *   Test migrations (if you have a local PostgreSQL instance configured via `DATABASE_URL`): `python manage.py migrate`
    *   Run the Gunicorn server: `gunicorn DJANGO_PROJECT.wsgi:application`

2.  **To fully simulate, set environment variables locally:**
    *   `DJANGO_SECRET_KEY`
    *   `DJANGO_DEBUG=False`
    *   `DATABASE_URL` (pointing to a local PostgreSQL instance if you want to test database interaction)
    *   `DJANGO_ALLOWED_HOST` (e.g., `localhost,127.0.0.1`)

    Then run:
    ```powershell
    ./build.sh 
    # If on Windows and build.sh gives trouble, execute commands manually or via WSL:
    # pip install -r requirements.txt
    # python manage.py collectstatic --noinput --clear
    # python manage.py migrate
    
    gunicorn DJANGO_PROJECT.wsgi:application
    ```

### Important Notes for Render:
*   **Free Tier Limitations**: Render's free tier services may spin down after a period of inactivity, leading to a delay on the first request after a while. PostgreSQL on the free tier has limited storage and connections.
*   **Static Files**: `WhiteNoise` is configured to serve static files. `build.sh` runs `collectstatic`.
*   **Database Migrations**: `build.sh` runs `migrate`.
*   **Logging**: Check your application logs in the Render dashboard for any deployment or runtime errors.
*   **`runtime.txt`**: Specifies the Python version for Render to use.
*   **`Procfile`**: While Render can use the start command directly, a `Procfile` is good practice and is referenced by some tooling. Render will use the "Start Command" field in the dashboard, which should match the `Procfile`'s web process.
*   **`build.sh`**: This script is crucial. Ensure it's executable (Git should handle this if you added it correctly: `git add --chmod=+x build.sh`). It prepares your application by installing dependencies, collecting static files, and running database migrations.

## Local Development