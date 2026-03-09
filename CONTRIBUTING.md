# Contributing to US Stock Analyser

Thank you for your interest in contributing to US Stock Analyser! This document provides guidelines and instructions for contributing.

## 🌟 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
- Use a clear and descriptive title
- Provide detailed description of the proposed feature
- Explain why this enhancement would be useful
- Include examples or mockups if possible

### Pull Requests

1. **Fork the repository**
   ```bash
   git fork https://github.com/yourusername/US-stock-analyser.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourAmazingFeature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   streamlit run app.py
   ```
   - Test with multiple stock symbols
   - Verify error handling works
   - Check UI responsiveness

5. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
   Use clear, descriptive commit messages

6. **Push to your fork**
   ```bash
   git push origin feature/YourAmazingFeature
   ```

7. **Open a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Keep functions focused and modular
- Add docstrings to functions

### Testing

- Test with various stock symbols (tech, finance, automotive, etc.)
- Test error cases (invalid symbols, API failures)
- Verify all three columns render correctly
- Check mobile responsiveness

### Documentation

- Update README.md if adding features
- Add comments for complex algorithms
- Update requirements.txt for new dependencies

## 🎯 Good First Issues

Looking for where to start? Consider:
- Adding more chart types (candlestick, bar charts)
- Implementing caching to reduce API calls
- Adding more financial metrics (P/E ratio, market cap)
- Improving error messages
- Adding unit tests
- Enhancing mobile UI

## 💬 Questions?

Feel free to:
- Open an issue for questions
- Reach out on [LinkedIn](https://www.linkedin.com/in/takako-kunugi-b901361b4/)

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

Thank you for contributing! 🎉
