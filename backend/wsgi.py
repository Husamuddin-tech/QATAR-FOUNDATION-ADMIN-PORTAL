"""WSGI entry point for production deployments"""
from app import create_app

# Create app instance for Vercel, Heroku, and other WSGI servers
app = create_app()

if __name__ == '__main__':
    app.run()
