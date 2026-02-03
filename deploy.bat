@echo off
echo ========================================
echo   CropGuard - GitHub Deployment
echo ========================================
echo.
echo This script will help you deploy to GitHub
echo.
echo Step 1: Create GitHub Repository
echo ---------------------------------
echo 1. Go to: https://github.com/new
echo 2. Repository name: CropGuard
echo 3. Description: Satellite-based crop health monitoring
echo 4. Choose: Public
echo 5. Don't initialize with README
echo 6. Click "Create repository"
echo.
echo Press any key when you've created the repository...
pause >nul
echo.
echo Step 2: Enter Your GitHub Username
echo ---------------------------------
set /p username="Enter your GitHub username: "
echo.
echo Step 3: Pushing to GitHub
echo ---------------------------------
echo.
git remote add origin https://github.com/%username%/CropGuard.git
git branch -M main
git push -u origin main
echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Your repository is now at:
echo https://github.com/%username%/CropGuard
echo.
echo Next Steps:
echo 1. Go to: https://streamlit.io/cloud
echo 2. Sign in with GitHub
echo 3. Click "New app"
echo 4. Select your CropGuard repository
echo 5. Click "Deploy"
echo.
echo Your app will be live in 2-3 minutes!
echo.
pause
