<div align="center">

# US Stock Analyser

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://us-stock-analyse.streamlit.app/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Live Demo](https://us-stock-analyse.streamlit.app/) | [Report Bug](https://github.com/yourusername/US-stock-analyser/issues) | [Request Feature](https://github.com/yourusername/US-stock-analyser/issues)

</div>

---

## Overview

US Stock Analyser is a Streamlit app for looking up financial data on US publicly traded companies. It pulls quarterly EPS and revenue figures directly from SEC EDGAR and uses OpenAI to summarize a company's main competitors.

### Features

- Quarterly EPS and revenue pulled straight from the SEC EDGAR XBRL API
- Dual-axis chart of EPS and revenue over the last 10 quarters
- Competitor summary generated with OpenAI
- Automatic charting for up to 5 competitor tickers
- Links out to Yahoo Finance and SEC filings for further reading

---

## Quick Start

### Try It Now

Visit the [live demo](https://us-stock-analyse.streamlit.app/) and enter any US stock ticker (e.g., AAPL, MSFT, GOOGL).

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/US-stock-analyser.git
   cd US-stock-analyser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**

   Create a `.streamlit/secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

---

## Technologies

| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core programming language |
| Streamlit | Web application framework |
| Pandas | Data manipulation and analysis |
| Matplotlib | Data visualization |
| OpenAI API | Competitor summary generation |
| SEC EDGAR API | Financial data source |
| NumPy | Numerical computing |

---

## Project Structure

```
US-stock-analyser/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .devcontainer/          # VS Code dev container config
    └── devcontainer.json
```

---

## Usage Examples

### Tech company
```
Input: AAPL
Output: Apple's quarterly trend, plus competitors such as MSFT and GOOGL
```

### Automotive company
```
Input: TSLA
Output: Tesla's quarterly trend, plus competitors such as F, GM, RIVN
```

### Financial sector
```
Input: JPM
Output: JPMorgan Chase's quarterly trend, plus other banking peers
```

---

## Configuration

### Environment Variables

The app requires an OpenAI API key for competitor analysis. Configure it in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-..."
```

### SEC API Headers

The SEC API requires a contact email in the User-Agent header. Update it in `app.py` if needed:

```python
headers = {"User-Agent": "your-email@example.com"}
```

---

## Data Sources

- **SEC EDGAR** - Official financial data from the U.S. Securities and Exchange Commission
- **OpenAI** - Competitor summaries
- **Yahoo Finance** - Additional research links

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Takako Kunugi**

- LinkedIn: [@takako-kunugi](https://www.linkedin.com/in/takako-kunugi-b901361b4/)
- GitHub: [@yourusername](https://github.com/yourusername)
