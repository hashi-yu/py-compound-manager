# Compound Management System - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd py-compound-manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your browser and go to: http://localhost:8081

## 🛠 Configuration

### Environment Variables
Create a `.env` file in the root directory (optional):
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/compounds.db
```

### Database
- The system uses SQLite by default
- Database file is created at `instance/compounds.db`
- No additional database setup required

## 🎯 Features

- **Compound Management**: Add, edit, view, and organize chemical compounds
- **Project Organization**: Group compounds into research projects
- **Molecular Calculations**: Automatic molecular weight calculation
- **Structure Images**: Upload and manage molecular structure images
- **Modern UI**: Apple-inspired design with responsive layout
- **Search & Filter**: Find compounds quickly
- **Data Export**: Export compound data

## 📁 File Structure

```
py-compound-manager/
├── app/                    # Main application
│   ├── models/            # Database models
│   ├── routes/            # URL routes and views
│   ├── templates/         # HTML templates
│   ├── static/           # CSS, JS, images
│   └── uploads/          # User uploaded files
├── config/               # Configuration files
├── instance/             # Database and instance-specific files
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
└── README.md            # Project documentation
```

## 🔧 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in run.py or kill existing process
   lsof -ti:8081 | xargs kill -9
   ```

2. **Database errors**
   ```bash
   # Reset database
   rm instance/compounds.db
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

3. **Missing dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## 📚 Usage Guide

### Adding Compounds
1. Click "Add Compound" button
2. Fill in compound information
3. Upload molecular structure image (optional)
4. Assign to project (optional)
5. Save

### Managing Projects
1. Go to "Projects" page
2. Create new project or edit existing ones
3. Organize compounds by project
4. View project statistics

### Molecular Weight Calculation
- Enter molecular formula (e.g., C6H6)
- System automatically calculates molecular weight
- Real-time validation and feedback

## 🔐 Security Notes

- Change default secret key in production
- Use proper database in production (PostgreSQL recommended)
- Set up proper file upload restrictions
- Configure HTTPS for production deployment

## 📞 Support

For issues or questions:
1. Check this setup guide
2. Review the troubleshooting section
3. Check application logs for error details

## 🚀 Production Deployment

For production use, consider:
- Using Gunicorn or uWSGI as WSGI server
- Setting up reverse proxy (Nginx)
- Using PostgreSQL or MySQL database
- Implementing proper backup strategy
- Setting up SSL/HTTPS
- Configuring environment variables properly