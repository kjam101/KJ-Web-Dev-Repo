from app import app, db

# Ensure the app context is properly set up
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")