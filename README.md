# 🧪 Compound Management System v2.2

> A modern, Apple-inspired chemical compound database system with hierarchical folder organization, refined Finder-style interface, and advanced molecular weight calculations.

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
- Spectral data file management

### 📁 **Hierarchical Folder System**
- Create nested folder structures for better organization
- Finder-style sidebar navigation with refined Apple design
- Drag-and-drop compound organization
- Folder-specific compound views (no subfolder mixing)
- Clean, intuitive folder tree visualization
- Smart folder badges showing compound counts

### 🎨 **Modern User Interface**
- Refined Apple-inspired design system
- Responsive layout for all devices
- Enhanced search and local sorting functionality
- Streamlined controls with better visual hierarchy
- Real-time form validation
- Polished buttons and interactive elements

### ⚡ **Advanced Features**
- High-precision molecular weight calculation
- Image preview and management
- Comprehensive file format support (50+ types)
- Extension-less file support (fid, log, propcar)
- User feedback system
- macOS auto-startup integration

## 🚀 Quick Start

### Simple Installation

1. **Download**: Download ZIP from GitHub or `git clone`
2. **Requirements**: Python 3.8+ only
3. **Launch**: Double-click `start.command` (macOS/Linux)
4. **Access**: http://localhost:8081

**One-click setup** - All dependencies installed automatically!

### 🔄 Auto-Start Setup (macOS)

**Set up automatic startup at login:**
```bash
./setup-autostart.command
```

**Disable auto-startup:**
```bash
./disable-autostart.command
```

**Access via bookmark:** Add `http://localhost:8081` to your browser bookmarks for instant access!

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

### Uploading Spectral Data
1. Open any compound detail page
2. Click **"Upload Data"**
3. Select data type (NMR, IR, MS, etc.)
4. Upload file (supports 50+ formats including fid, log, propcar)
5. Add optional notes

### Managing Folders
1. Use the refined sidebar to navigate folder hierarchy
2. Create new folders with the compact "+" button
3. Drag compounds between folders for easy organization
4. Each folder shows only direct compounds (no subfolder mixing)
5. Smart badges display compound counts for each folder

### Molecular Weight Calculation
- Enter molecular formula (e.g., `C6H6`)
- System automatically calculates molecular weight
- Real-time validation provides feedback
- High-precision calculations with confidence levels

## 📁 Project Structure

```
py-compound-manager/
├── app/                    # Main application
│   ├── models/            # Database models (Compound, Folder, SpectralData)
│   ├── routes/            # URL routes and API endpoints
│   ├── templates/         # HTML templates (Finder-style interface)
│   ├── static/           # CSS, JavaScript, images
│   └── uploads/          # User uploaded files
│       ├── data/         # Spectral data files
│       └── structures/   # Molecular structure images
├── config/               # Configuration files
├── instance/             # Database and instance files
│   └── feedback/         # User feedback storage
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
├── start.command         # One-click launcher (macOS/Linux)
├── setup-autostart.command    # Auto-startup setup (macOS)
├── disable-autostart.command  # Disable auto-startup (macOS)
└── README.md            # This file
```

## 🔧 API Endpoints

### Compounds
- `GET /` - List all compounds
- `GET /compound/<id>` - View compound details
- `POST /add` - Add new compound
- `POST /edit/<id>` - Edit compound

### Folders
- `GET /?folder_id=<id>` - View folder contents
- `POST /add_folder` - Add new folder
- `POST /edit_folder/<id>` - Edit folder
- `POST /move_compound` - Move compound between folders

### Spectral Data
- `POST /upload_data/<compound_id>` - Upload spectral data
- `GET /download/<data_id>` - Download data file
- `POST /delete_spectral_data/<data_id>` - Delete data file

### API
- `POST /api/calculate-molecular-weight` - Calculate molecular weight
- `POST /api/validate-molecular-formula` - Validate formula
- `POST /api/feedback` - Submit user feedback
- `GET /admin/feedback` - View feedback (admin)

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

- [x] Spectral data management
- [x] Multi-format file support (50+ types)
- [x] Auto-startup system (macOS)
- [x] User feedback system
- [x] Hierarchical folder system
- [x] Refined Finder-style interface
- [x] Enhanced search and local sorting
- [ ] Advanced search and filtering
- [ ] Data export to multiple formats
- [ ] Integration with chemical databases
- [ ] Collaborative features
- [ ] Mobile application
- [ ] Advanced molecular visualization

## 📂 Supported File Formats

### Spectral Data
- **NMR Data:** fid (extension-less), .jdx, .dx
- **Binary Data:** .bin, .dat, .raw, .spc
- **Text Data:** .txt, .csv, .log, propcar, text
- **Archives:** .zip, .tar, .gz, .bz2
- **Scientific:** .h5, .hdf5, .npz, .npy, .mat
- **Documents:** .pdf, .xlsx, .xls, .docx, .doc, .ppt, .pptx

### Structure Images
- **Images:** .png, .jpg, .jpeg, .gif

## 🏆 Acknowledgments

- Built with Flask and SQLAlchemy
- UI inspired by Apple's design principles
- Molecular weight calculations using scientific databases
- Community contributions and feedback

---

**Happy researching! 🧬**