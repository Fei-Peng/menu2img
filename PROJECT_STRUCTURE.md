# Menu2Img Project Structure

## 📁 Directory Organization

```
menu2img/
├── 📁 src/                          # Source code
│   ├── 📁 web/                      # Web application
│   │   ├── app.py                   # Flask web server
│   │   └── templates/               # HTML templates
│   │       └── index.html           # Main web interface
│   ├── 📁 desktop/                  # Desktop application
│   │   ├── main.js                  # Electron main process
│   │   ├── preload.js               # Electron preload script
│   │   └── renderer.js              # Desktop app enhancements
│   └── 📁 shared/                   # Shared components
│       ├── menu2img.py              # CLI version
│       └── requirements.txt         # Python dependencies
├── 📁 assets/                       # Static assets
│   ├── 📁 icons/                    # App icons
│   │   ├── icon.icns               # macOS icon
│   │   ├── icon.ico                # Windows icon
│   │   └── icon.png                # Linux icon
│   └── 📁 images/                   # Sample images
├── 📁 docs/                         # Documentation
│   └── README.md                    # Main documentation
├── 📁 scripts/                      # Utility scripts
│   └── start-web.sh                 # Web app startup script
├── 📁 uploads/                      # Temporary upload storage
├── 📁 dishes/                       # Generated images
├── 📁 dist/                         # Build outputs (created by electron-builder)
├── package.json                     # Node.js dependencies & build config
├── PROJECT_STRUCTURE.md             # This file
└── upload_history.json              # Upload tracking data
```

## 🎯 Purpose of Each Directory

### **src/web/**
Contains the Flask web application:
- **app.py**: Main Flask server with API endpoints
- **templates/**: HTML templates for the web interface

### **src/desktop/**
Contains the Electron desktop application:
- **main.js**: Main Electron process (window management, Python backend)
- **preload.js**: Secure communication bridge
- **renderer.js**: Desktop app UI enhancements

### **src/shared/**
Contains components used by both web and desktop:
- **menu2img.py**: Command-line interface version
- **requirements.txt**: Python package dependencies

### **assets/**
Static files for the application:
- **icons/**: Application icons for different platforms
- **images/**: Sample images and graphics

### **docs/**
Documentation files:
- **README.md**: Comprehensive project documentation

### **scripts/**
Utility scripts for development and deployment:
- **start-web.sh**: Easy web app startup script

## 🚀 How to Run

### **Web App:**
```bash
# Option 1: Use the startup script
./scripts/start-web.sh

# Option 2: Manual start
cd src/web
python app.py
```

### **Desktop App:**
```bash
# Development mode
npm run dev

# Production build
npm run build
```

### **Install Dependencies:**
```bash
# All dependencies
npm run install-deps

# Python only
pip install -r src/shared/requirements.txt

# Node.js only
npm install
```

## 🔄 File Relationships

- **Web App**: `src/web/app.py` → `src/web/templates/index.html`
- **Desktop App**: `src/desktop/main.js` → `src/web/app.py` (Python backend)
- **Shared Logic**: Both apps use functions from `src/shared/`
- **Assets**: Both apps reference files from `assets/`

## 📦 Build Process

1. **Web App**: Direct Python execution
2. **Desktop App**: Electron packages the web app + Python backend
3. **Distribution**: `electron-builder` creates platform-specific installers

## 🎨 Benefits of This Structure

- **Separation of Concerns**: Web, desktop, and shared code are clearly separated
- **Maintainability**: Easy to find and modify specific components
- **Scalability**: Easy to add new features or platforms
- **Documentation**: Clear organization makes the project self-documenting
- **Build Process**: Clean separation between development and distribution files 