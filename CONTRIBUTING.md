# Contributing to Menu2Img

Thank you for your interest in contributing to Menu2Img! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/menu2img.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes
5. **Test** your changes thoroughly
6. **Commit** with a clear message: `git commit -m "Add amazing feature"`
7. **Push** to your fork: `git push origin feature/amazing-feature`
8. **Create** a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/menu2img.git
cd menu2img

# Install dependencies
npm run install-deps

# Set your OpenAI API key
export OPENAI_API_KEY=your_api_key_here
```

### Running the Applications

#### Web App
```bash
# Option 1: Use the startup script
./scripts/start-web.sh

# Option 2: Manual start
cd src/web
python app.py
```

#### Desktop App
```bash
# Development mode
npm run dev

# Build for distribution
npm run build
```

## 📁 Project Structure

```
src/
├── web/           # Flask web application
├── desktop/       # Electron desktop app
└── shared/        # Shared components
```

## 🧪 Testing

### Web App Testing
```bash
cd src/web
python -c "import app; print('Web app imports successfully')"
```

### Desktop App Testing
```bash
npm test
```

## 📝 Code Style

### Python
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### JavaScript
- Use ES6+ features
- Follow consistent naming conventions
- Add JSDoc comments for functions
- Use meaningful variable names

### HTML/CSS
- Use semantic HTML
- Follow BEM methodology for CSS
- Keep styles organized and commented

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description** of the issue
2. **Steps** to reproduce
3. **Expected** behavior
4. **Actual** behavior
5. **Environment** details (OS, Python version, Node version)
6. **Screenshots** if applicable

## 💡 Feature Requests

When requesting features, please include:

1. **Description** of the feature
2. **Use case** and benefits
3. **Implementation** suggestions (if any)
4. **Mockups** or examples (if applicable)

## 🔧 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No sensitive data is included

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Web app tested
- [ ] Desktop app tested
- [ ] CLI tested

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have made corresponding changes to documentation
```

## 📚 Documentation

When adding new features, please update:

1. **README.md** - Main documentation
2. **PROJECT_STRUCTURE.md** - If structure changes
3. **Code comments** - Inline documentation
4. **API documentation** - If adding new endpoints

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

## 📄 License

By contributing to Menu2Img, you agree that your contributions will be licensed under the MIT License.

## 🙏 Acknowledgments

Thank you for contributing to Menu2Img! Your contributions help make this project better for everyone.

## 📞 Getting Help

If you need help with contributing:

1. Check existing issues and discussions
2. Create a new issue with the "help wanted" label
3. Join our community discussions

---

**Happy coding! 🍽️✨** 