# Deploying to Render with Cloudinary Integration

## Required Environment Variables for Render

When deploying to Render, you need to set the following environment variables in your Render dashboard:

### Core Django Settings
- `DJANGO_SECRET_KEY` - A strong, unique secret key for your application
- `DJANGO_DEBUG` - Set to "False" for production environments
- `DJANGO_ALLOWED_HOSTS` - Your custom domain(s), comma-separated (optional, Render handles this)

### Database Settings
- `DATABASE_URL` - Automatically provided by Render if using their PostgreSQL service

### Cloudinary Settings (Choose ONE of these options)

**Option 1: Single Cloudinary URL (RECOMMENDED)**
- `CLOUDINARY_URL` - In the format: `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`
  - For example: `cloudinary://123456789012345:abcdefghijklmnopqrstuv@example-cloud`

**Option 2: Individual Cloudinary Credentials**
- `CLOUDINARY_CLOUD_NAME` - Your Cloudinary cloud name
- `CLOUDINARY_API_KEY` - Your Cloudinary API key
- `CLOUDINARY_API_SECRET` - Your Cloudinary API secret

### Email Settings (Optional)
- `DJANGO_EMAIL_BACKEND` - Default is SMTP
- `DJANGO_EMAIL_HOST` - Default is smtp.gmail.com
- `DJANGO_EMAIL_PORT` - Default is 587
- `DJANGO_EMAIL_USE_TLS` - Default is True
- `EMAIL_HOST_USER` - Your email address
- `EMAIL_HOST_PASSWORD` - Your email password or app password

## Step-by-step Deployment Guide

1. **Create a Render Account**
   - Sign up at [render.com](https://render.com) if you haven't already

2. **Set Up a Web Service**
   - Create a new Web Service
   - Connect your GitHub repository
   - Configure your service:
     - **Name**: Your project name
     - **Runtime**: Python
     - **Build Command**: `./build.sh`
     - **Start Command**: `cd DJANGO_PROJECT && gunicorn DJANGO_PROJECT.wsgi:application`

3. **Configure Environment Variables**
   - In your Render dashboard, go to the Environment section
   - Add all required environment variables, especially the `CLOUDINARY_URL`
   - Make sure to set `DJANGO_DEBUG=False`

4. **Set Up a PostgreSQL Database (Optional)**
   - Create a new PostgreSQL database in Render
   - Render will automatically add the DATABASE_URL to your web service

5. **Deploy Your Service**
   - Click "Create Web Service" and wait for the deployment to complete
   - The first deployment may take a few minutes

## Troubleshooting Profile Picture Updates

If profile pictures are not updating after deployment:

1. **Check the Render Logs**
   - Go to your Render dashboard > Logs
   - Look for any errors related to Cloudinary or media uploads

2. **Verify Cloudinary Configuration**
   - Confirm that the `CLOUDINARY_URL` environment variable is correctly set in Render
   - Format should be: `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`
   - Make sure there are no typos or extra characters

3. **Test Your Cloudinary Connection**
   - Locally, run the `cloudinary_test.py` script to validate your credentials
   - If it works locally but not on Render, it's likely an environment variable issue

4. **Check Debug Mode**
   - Make sure `DJANGO_DEBUG` is set to "False" in production
   - The code is configured to use Cloudinary only when DEBUG is False

5. **Clear Your Browser Cache**
   - Sometimes browser caching can prevent updated images from showing
   - Try a hard refresh (Ctrl+F5) or clear your browser cache

6. **Default Profile Image**
   - The application is configured to automatically upload the default profile image (`default.jpg`) to Cloudinary during startup
   - If you're still seeing issues with the default profile picture, run `python manage.py ensure_default_profile_image` after deployment
   - Alternatively, run the `post_deploy.sh` script to handle this automatically
   
7. **Manual Default Image Upload**
   - If automated uploads fail, you can manually upload a default image to Cloudinary
   - Name it exactly `default.jpg` and upload it to the `media` folder in your Cloudinary account

## Common Issues and Solutions

### "Unknown API key API_KEY" Error
This typically means that the environment variable for Cloudinary is not set correctly or is not being parsed properly.

Solution:
- Double-check the format of your `CLOUDINARY_URL` in the Render dashboard
- Ensure there are no extra quotes, spaces, or special characters in the environment variable
- The format should be exactly: `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`

### Import Errors for Cloudinary_Storage
This means that the `django-cloudinary-storage` package is not installed or not accessible.

Solution:
- Ensure that `django-cloudinary-storage` and `cloudinary` are in your `requirements.txt` file
- Check the build logs to make sure the packages are being installed during deployment

### Media Files Not Being Served
This could happen if Cloudinary is configured correctly but the media URL is not being generated properly.

Solution:
- Ensure that `DEFAULT_FILE_STORAGE` is set to `"cloudinary_storage.storage.MediaCloudinaryStorage"` in production
- Check that the `CLOUDINARY_STORAGE` dictionary has all required fields (CLOUD_NAME, API_KEY, API_SECRET)
- Verify that your templates are using the correct URL pattern for media files
