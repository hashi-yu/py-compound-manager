# 🧪 Compound Management System v2.0

> A modern, Apple-inspired chemical compound database system with advanced molecular weight calculations and project management capabilities.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/flask-2.3+-orange.svg)

## ✨ Features

### 🔬 **Compound Management**
- Add, edit, and organize chemical compounds
- Upload molecular structure images
- Automatic molecular weight calculation
- Real-time molecular formula validation
- Notes and comments system

### 📊 **Project Organization**
- Group compounds by research projects
- Project statistics and overview
- Advanced filtering and search
- Export functionality

### 🎨 **Modern User Interface**
- Apple-inspired design system
- Responsive layout for all devices
- Real-time form validation
- Intuitive navigation

### ⚡ **Advanced Features**
- High-precision molecular weight calculation
- Image preview and management
- Data backup and restore
- Multi-format file support

## 🚀 Quick Start

### Simple Installation

1. **Download**: Download ZIP from GitHub or `git clone`
2. **Requirements**: Python 3.8+ only
3. **Launch**: Double-click `start.command` (macOS/Linux)
4. **Access**: http://localhost:8081

**One-click setup** - All dependencies installed automatically!

## 📖 Detailed Installation

### Step-by-Step Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

4. **Run Application**
   ```bash
   python run.py
   ```

## 🛠 Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:

```env
# Security
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///instance/compounds.db

# File Uploads
MAX_CONTENT_LENGTH=16777216

# Server
HOST=127.0.0.1
PORT=8081
```

## 📱 Usage Guide

### Adding Compounds
1. Click **"Add Compound"**
2. Enter compound name and molecular formula
3. Upload structure image (optional)
4. Assign to project (optional)
5. Add notes and save

### Managing Projects
1. Navigate to **"Projects"**
2. Create new projects or edit existing ones
3. View project statistics
4. Organize compounds by research areas

### Molecular Weight Calculation
- Enter molecular formula (e.g., `C6H6`)
- System automatically calculates molecular weight
- Real-time validation provides feedback
- High-precision calculations with confidence levels

## 📁 Project Structure

```
py-compound-manager/
├── app/                    # Main application
│   ├── models/            # Database models (Compound, Project)
│   ├── routes/            # URL routes and API endpoints
│   ├── templates/         # HTML templates
│   ├── static/           # CSS, JavaScript, images
│   └── uploads/          # User uploaded files
├── config/               # Configuration files
├── instance/             # Database and instance files
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
├── setup.sh             # Setup script (Unix)
├── setup_windows.bat    # Setup script (Windows)
└── README.md            # This file
```

## 🔧 API Endpoints

### Compounds
- `GET /` - List all compounds
- `GET /compound/<id>` - View compound details
- `POST /add` - Add new compound
- `POST /edit/<id>` - Edit compound

### Projects
- `GET /projects` - List all projects
- `POST /add_project` - Add new project
- `POST /edit_project/<id>` - Edit project

### API
- `POST /api/calculate-molecular-weight` - Calculate molecular weight
- `POST /api/validate-molecular-formula` - Validate formula

## 🚀 Deployment

### Development
```bash
python run.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8081 "app:create_app()"
```

### Docker
```bash
docker build -t compound-manager .
docker run -p 8081:8081 compound-manager
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Troubleshooting

**Port already in use:**
```bash
# Kill process using port 8081
lsof -ti:8081 | xargs kill -9
```

**Database issues:**
```bash
# Reset database
rm instance/compounds.db
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

**Dependencies issues:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Getting Help
- Create an issue on GitHub
- Check the [Security Guide](SECURITY.md)
- Review application logs

## 🎯 Roadmap

- [ ] Advanced search and filtering
- [ ] Data export to multiple formats
- [ ] Integration with chemical databases
- [ ] Collaborative features
- [ ] Mobile application
- [ ] Advanced molecular visualization

## 🏆 Acknowledgments

- Built with Flask and SQLAlchemy
- UI inspired by Apple's design principles
- Molecular weight calculations using scientific databases
- Community contributions and feedback

---

**Happy researching! 🧬**