# Deploy Django Project to Render
Write-Host "Preparing for deployment to Render..." -ForegroundColor Green

# Check packages for deployment
try {
    Import-Module PackageManagement -ErrorAction SilentlyContinue
    Write-Host "Checking deployment requirements..." -ForegroundColor Yellow
    
    # Test if the required deployment packages are installed in the Python environment
    $deploymentPackages = @("dj-database-url", "whitenoise", "gunicorn", "psycopg2-binary")
    $installMissing = $false
    
    foreach ($package in $deploymentPackages) {
        try {
            $output = python -c "import $($package.Replace('-', '_'))" 2>&1
            Write-Host "✓ $package installed" -ForegroundColor Green
        } catch {
            Write-Host "✗ $package not installed" -ForegroundColor Yellow
            $installMissing = $true
        }
    }
    
    if ($installMissing) {
        Write-Host "Some deployment packages are missing. Would you like to install them? (Y/N)" -ForegroundColor Yellow
        $installResponse = Read-Host
        if ($installResponse -eq "Y" -or $installResponse -eq "y") {
            Write-Host "Installing missing packages..." -ForegroundColor Yellow
            pip install dj-database-url whitenoise gunicorn psycopg2-binary
        }
    }
}
catch {
    Write-Host "Warning: Unable to check deployment packages" -ForegroundColor Yellow
}

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "Git is installed ✓" -ForegroundColor Green
}
catch {
    Write-Host "Error: Git is not installed. Please install Git and try again." -ForegroundColor Red
    exit 1
}

# Check if the project is already a git repository
if (-not (Test-Path .git)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit for Render deployment"
    Write-Host "Git repository initialized ✓" -ForegroundColor Green
}
else {
    Write-Host "Git repository already exists ✓" -ForegroundColor Green
    # Stage changes
    Write-Host "Staging changes..." -ForegroundColor Yellow
    git add .
    git commit -m "Updates for Render deployment"
    Write-Host "Changes committed ✓" -ForegroundColor Green
}

# Instructions for Render deployment
Write-Host "`nNext steps for deployment to Render:" -ForegroundColor Cyan
Write-Host "1. Create a Render account at https://render.com if you haven't already" -ForegroundColor White
Write-Host "2. In your Render dashboard, click on 'New +' and select 'Blueprint'" -ForegroundColor White
Write-Host "3. Connect your Git repository (GitHub, GitLab, or Bitbucket)" -ForegroundColor White
Write-Host "4. Select the repository with your Django project" -ForegroundColor White
Write-Host "5. Render will automatically detect the render.yaml file and set up your services" -ForegroundColor White
Write-Host "6. Click 'Apply' to start the deployment process" -ForegroundColor White
Write-Host "`nYour application will be available at: https://blog-app.onrender.com" -ForegroundColor Green

Write-Host "`nDo you want to open the Render dashboard now? (Y/N)" -ForegroundColor Yellow
$response = Read-Host
if ($response -eq "Y" -or $response -eq "y") {
    Start-Process "https://dashboard.render.com/"
    Write-Host "Render dashboard opened in your browser" -ForegroundColor Green
}

Write-Host "`nDeployment preparation complete!" -ForegroundColor Green
Write-Host "After your app is deployed, remember to create a superuser account in the Render shell:" -ForegroundColor Yellow
Write-Host "python manage.py createsuperuser" -ForegroundColor Cyan