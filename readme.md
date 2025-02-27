# Ztudy

Ztudy is an online self-learning environment that enables users to create and customize their own study space anytime, anywhere. The platform provides tools and resources to help learners structure their study sessions effectively.

## Key Features

- Collaborative Study Rooms: Choose between solo study or shared study spaces with others.

- Personalized Study Environment: Organize and manage your learning space.
- Notes & Resources: Save important notes and access useful study materials.
- Time Management: Plan and track your study sessions efficiently.
- Notification System: Stay on top of your learning schedule with reminders.
---
✨ **Ztudy - Build Your Perfect Study Space!** ✨

# Django Project Setup on Windows

This guide provides step-by-step instructions on how to set up and run a Django project on Windows.

## Step 1: Create and Activate Virtual Environment

```sh
# Navigate to your project folder
cd path\to\your\project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

## Step 2: Install Dependencies

```sh
pip install -r requirements.txt
```

## Step 3: Create and Configure Environment Variables

```sh
# Copy .env.example to .env
copy .env.example .env
```

Update the `.env` file with your project-specific settings.

## Step 4: Apply Migrations

```sh
# Apply database migrations
python manage.py migrate
```

## Step 5: Create a Superuser (Optional)

```sh
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

## Step 6: Run the Development Server

```sh
python manage.py runserver
```

By default, the server runs at `http://127.0.0.1:8000/`.
