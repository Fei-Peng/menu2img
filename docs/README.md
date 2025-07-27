# Menu2Img - AI-Powered Menu to Food Image Generator

Generate beautiful, appetizing food photos from menu images using AI. Upload a menu photo and get professional food images for each dish!

## 🌟 Features

- **Smart Menu Extraction**: Uses GPT-4 Vision to intelligently extract dish names
- **AI Image Generation**: Creates beautiful food photos with DALL-E 3
- **Smart Caching**: Saves API costs by reusing previously generated images
- **File Tracking**: Remembers uploaded menus to avoid reprocessing
- **Web & Desktop**: Available as both web app and native desktop application
- **Responsive Design**: Works perfectly on all devices

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** (for desktop app)
3. **OpenAI API Key** with access to GPT-4 Vision and DALL-E 3

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd menu2img
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY=sk-your_openai_api_key_here
   ```

## 🌐 Web App

### Run the Web App

```bash
python app.py
```

Then open http://localhost:5051 in your browser.

### Web App Features

- Drag & drop file upload
- Real-time processing with progress indicators
- Beautiful 3-column grid layout for generated images
- Collapsible menu items list
- Original image display
- Smart caching with visual indicators

## 🖥️ Desktop App

### Install Dependencies

```bash
npm install
```

### Development Mode

```bash
npm run dev
```

This will start both the Python backend and the Electron app.

### Build Desktop App

```bash
# Build for current platform
npm run build

# Build for specific platforms
npm run build-mac    # macOS
npm run build-win    # Windows
npm run build-linux  # Linux
```

### Desktop App Features

- **Native File Dialog**: Use system file picker
- **Custom Title Bar**: App-specific window controls
- **Menu Bar**: About, Help, and utility functions
- **Keyboard Shortcuts**: 
  - `Ctrl/Cmd + O`: Open file
  - `Ctrl/Cmd + Q`: Quit app
- **Automatic Backend**: Python server starts automatically

## 📁 Project Structure

```
menu2img/
├── app.py                 # Flask web application
├── menu2img.py           # CLI version
├── main.js               # Electron main process
├── preload.js            # Electron preload script
├── renderer.js           # Desktop app enhancements
├── package.json          # Node.js dependencies
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary upload storage
├── dishes/               # Generated images
└── upload_history.json   # Upload tracking data
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### API Models Used

- **GPT-4 Vision**: For menu text extraction
- **DALL-E 3**: For food image generation

## 💡 Usage

1. **Upload a Menu Image**: Drag & drop or click to browse
2. **AI Processing**: The app extracts dish names using GPT-4 Vision
3. **Image Generation**: DALL-E 3 creates beautiful food photos
4. **Results**: View original menu, extracted dishes, and generated images

## 🎯 Smart Features

### Caching System

- **Image Caching**: Reuses previously generated images
- **File Tracking**: Remembers uploaded menus by content hash
- **Upload History**: Tracks how many times each menu was processed

### File Management

- **Automatic Cleanup**: Temporary files are managed automatically
- **Persistent Storage**: Generated images and history are preserved
- **Error Handling**: Graceful handling of API failures and timeouts

## 🛠️ Development

### Web App Development

```bash
python app.py
# App runs on http://localhost:5051
```

### Desktop App Development

```bash
npm run dev
# Starts both backend and Electron app
```

### Building for Distribution

```bash
npm run build
# Creates distributable packages in dist/ folder
```

## 📊 Performance

- **First Upload**: Normal processing time (30-60 seconds)
- **Cached Results**: Instant response (0-2 seconds)
- **API Efficiency**: Only generates new images when needed
- **Memory Usage**: Lightweight, efficient processing

## 🔒 Security

- **Content Isolation**: Secure communication between processes
- **File Validation**: Checks file types and sizes
- **API Key Protection**: Environment variable storage
- **Error Handling**: Graceful failure modes

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not set"**
   - Set the `OPENAI_API_KEY` environment variable

2. **"No dishes found"**
   - Check image quality and menu clarity
   - Ensure menu items are clearly visible

3. **"Request timed out"**
   - Check internet connection
   - Try with a smaller image file

4. **Desktop app won't start**
   - Ensure Python and Node.js are installed
   - Check that all dependencies are installed

### Debug Mode

```bash
# Web app with debug logging
python app.py

# Desktop app with DevTools
npm run dev
```

## 📈 Future Enhancements

- [ ] Batch processing for multiple menus
- [ ] Custom image styles and prompts
- [ ] Export to various formats
- [ ] Integration with restaurant management systems
- [ ] Mobile app version

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT-4 Vision and DALL-E 3 APIs
- Flask for the web framework
- Electron for the desktop app framework
- The open source community for inspiration and tools

---

**Made with ❤️ for food lovers and restaurant owners everywhere!** 