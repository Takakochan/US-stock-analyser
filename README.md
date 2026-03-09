<div align="center">

# 📈 US Stock Analyser

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://us-stock-analyse.streamlit.app/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-green.svg)](https://github.com/yourusername/US-stock-analyser)

**Real-time financial analysis with AI-powered competitive insights**

[Live Demo](https://us-stock-analyse.streamlit.app/) | [Report Bug](https://github.com/yourusername/US-stock-analyser/issues) | [Request Feature](https://github.com/yourusername/US-stock-analyser/issues)

</div>

---

## 🎯 Overview

US Stock Analyser is an interactive web application that provides comprehensive financial analysis for publicly traded US companies. Built with Streamlit and powered by real-time SEC data and OpenAI, it offers instant insights into company performance and competitive landscapes.

### ✨ Key Features

- **📊 Real-Time Financial Data** - Direct integration with SEC EDGAR API for accurate, up-to-date financial metrics
- **📈 Interactive Visualizations** - Beautiful dual-axis charts showing EPS and Revenue trends over 10 quarters
- **🤖 AI-Powered Insights** - OpenAI integration for intelligent competitor analysis
- **🔍 Competitive Intelligence** - Automatic comparison with top 5 industry competitors
- **📱 Responsive Design** - Clean, modern interface that works on all devices
- **🔗 External Resources** - Direct links to Yahoo Finance and SEC filings

---

## 🚀 Quick Start

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

## 🖼️ Screenshots

### Main Interface
*Enter a stock symbol to view comprehensive financial analysis*

![App Interface](https://via.placeholder.com/800x400/FE53BB/FFFFFF?text=Add+Screenshot+Here)

### Example Analysis
*EPS and Revenue trends with AI-powered competitor insights*

![Analysis View](https://via.placeholder.com/800x400/0040ff/FFFFFF?text=Add+Screenshot+Here)

> **Note:** Replace placeholder images with actual screenshots of your app

---

## 🛠️ Technologies

| Technology | Purpose |
|------------|---------|
| **Python 3.11+** | Core programming language |
| **Streamlit** | Web application framework |
| **Pandas** | Data manipulation and analysis |
| **Matplotlib** | Data visualization |
| **OpenAI API** | AI-powered competitor analysis |
| **SEC EDGAR API** | Real-time financial data source |
| **NumPy** | Numerical computing |

---

## 📂 Project Structure

```
US-stock-analyser/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .devcontainer/         # VS Code dev container config
    └── devcontainer.json
```

---

## 💡 Usage Examples

### Analyze a Tech Giant
```
Input: AAPL
Output: Apple Inc. financial trends + competitors (MSFT, GOOGL, etc.)
```

### Compare Automotive Companies
```
Input: TSLA
Output: Tesla financial data + competitors (F, GM, RIVN, etc.)
```

### Research Financial Sector
```
Input: JPM
Output: JPMorgan Chase metrics + banking sector competitors
```

---

## 🔧 Configuration

### Environment Variables

The app requires an OpenAI API key for competitor analysis. Configure it in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-..."
```

### SEC API Headers

The app uses a custom User-Agent header for SEC API requests. Update in `app.py` if needed:

```python
headers = {"User-Agent": "your-email@example.com"}
```

---

## 📊 Data Sources

- **SEC EDGAR** - Official financial data from U.S. Securities and Exchange Commission
- **OpenAI GPT-3.5** - Competitive intelligence and market analysis
- **Yahoo Finance** - Additional research links and resources

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Takako Kunugi**

- LinkedIn: [@takako-kunugi](https://www.linkedin.com/in/takako-kunugi-b901361b4/)
- GitHub: [@yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- SEC EDGAR for providing free access to financial data
- OpenAI for powering intelligent analysis
- Streamlit for the amazing web framework
- The open-source community for inspiration and support

---

<div align="center">

**⭐ Star this repo if you find it helpful!**



</div>
