# Ztudy

Ztudy is an online self-learning environment that enables users to create and customize their own study space anytime, anywhere. The platform provides tools and resources to help learners structure their study sessions effectively.

## Key Features

- **Collaborative Study Rooms**: Choose between solo study or shared study spaces with others.
- **Personalized Study Environment**: Organize and manage your learning space.
- **Notes & Resources**: Save important notes and access useful study materials.
- **Time Management**: Plan and track your study sessions efficiently.
- **Notification System**: Stay on top of your learning schedule with reminders.
- **Social Learning**: Connect with other learners and share study experiences.
- **Progress Tracking**: Monitor your study habits and achievements over time.
- **Customizable Backgrounds**: Personalize your study environment with various themes.

## Tech Stack

- **Backend**: Django, Django REST Framework, Channels (WebSockets)
- **Database**: MySQL
- **Authentication**: JWT, Google OAuth
- **Real-time Communication**: WebSockets
- **Cloud Storage**: Cloudinary
- **Video Conferencing**: Agora
- **Task Scheduling**: Celery, Redis

## Project Setup

### Prerequisites

- Python 3.12+
- MySQL 8.0+
- Redis (for Celery)

### Development Environment Setup

#### Backend Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/BuiBao3103/ztudy-be.git
   cd ztudy
   ```

2. **Create and activate virtual environment**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```sh
   # Copy .env.example to .env
   copy .env.example .env
   ```
   Update the `.env` file with your project-specific settings.

5. **Apply migrations**
   ```sh
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```sh
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```sh
   python manage.py runserver
   ```

### Running Celery

Celery is used for background task processing and scheduled jobs in Ztudy. Here's how to set it up:

1. **Start Redis server**
   ```sh
   # Windows (if using WSL)
   sudo service redis-server start
   ```

2. **Start Celery worker**
   ```sh
   celery -A Ztudy worker -l info -P solo
   ```

3. **Start Celery beat for scheduled tasks**
   ```sh
   celery -A Ztudy beat -l info
   ```

## API Documentation

API documentation is available at `/api/v1/swagger/` when running the server. This provides a Swagger UI interface for exploring and testing the API endpoints.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

✨ **Ztudy - Build Your Perfect Study Space!** ✨
