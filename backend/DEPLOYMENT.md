# Deployment Guide

This guide will help you deploy your Django FJJK application to production.

## Option 1: Railway (Recommended)

Railway is the easiest platform for Django deployment with file uploads.

### Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Connect your GitHub repository
   - Railway will automatically detect it's a Django app
   - Add a PostgreSQL database service

3. **Set Environment Variables**
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   DB_NAME=railway
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   DB_HOST=your-db-host
   DB_PORT=5432
   ```

4. **Deploy**
   - Railway will automatically build and deploy
   - Your app will be available at `https://your-app-name.railway.app`

## Option 2: Heroku

### Steps:

1. **Install Heroku CLI**
   - Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-super-secret-key-here
   heroku config:set DEBUG=False
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

## Option 3: DigitalOcean App Platform

### Steps:

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://digitalocean.com)

2. **Create App**
   - Connect your GitHub repository
   - Choose Django as the app type
   - Add PostgreSQL database

3. **Configure Environment**
   - Set environment variables in the dashboard
   - Configure build and run commands

## Post-Deployment Steps

1. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

2. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

## Environment Variables

Set these in your deployment platform:

- `SECRET_KEY`: Django secret key (generate a new one)
- `DEBUG`: Set to `False` for production
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port (usually 5432)

## Security Notes

- Never commit your `SECRET_KEY` to version control
- Always set `DEBUG=False` in production
- Use environment variables for sensitive data
- Consider using a CDN for static files
- Set up proper CORS origins for your frontend

## Troubleshooting

- Check logs in your deployment platform
- Ensure all environment variables are set
- Verify database connection
- Check that static files are being served correctly
