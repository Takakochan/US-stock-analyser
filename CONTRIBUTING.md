# Contributing to US Stock Analyser

Thanks for your interest in contributing. This document covers the basics of reporting bugs, suggesting changes, and submitting pull requests.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce it
- Expected vs. actual behavior
- Screenshots, if relevant
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

- Use a clear, descriptive title
- Describe the proposed feature
- Explain why it would be useful
- Include examples or mockups if you have them

### Pull Requests

1. **Fork the repository**
   ```bash
   git fork https://github.com/yourusername/US-stock-analyser.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for non-obvious logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   streamlit run app.py
   ```
   - Test with multiple stock symbols
   - Check that error handling still works
   - Check the UI at different window sizes

5. **Commit your changes**

   Use clear, descriptive commit messages.

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Describe what changed and why
   - Reference any related issues
   - Include screenshots for UI changes

## Development Guidelines

### Code Style

- Follow PEP 8
- Use meaningful variable and function names
- Keep functions focused and modular
- Add docstrings to functions

### Testing

- Test with various stock symbols (tech, finance, automotive, etc.)
- Test error cases (invalid symbols, API failures)
- Verify all three columns render correctly
- Check mobile/narrow-window layout

### Documentation

- Update README.md if adding features
- Add comments for complex algorithms
- Update requirements.txt for new dependencies

## Good First Issues

- Add more chart types (candlestick, bar charts)
- Add caching to reduce redundant API calls
- Add more financial metrics (P/E ratio, market cap)
- Improve error messages
- Add unit tests
- Improve the mobile layout

## Questions?

- Open an issue for questions
- Reach out on [LinkedIn](https://www.linkedin.com/in/takako-kunugi-b901361b4/)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

Thanks for contributing.
