# 🚀 Automated News Summarizer

**An intelligent Python-based system that automatically scrapes Bangla news articles and generates high-quality summaries.**

## 📋 Overview

This project automatically:
- Scrapes headlines and content from Bangla news websites
- Processes and cleans the text data
- Generates intelligent summaries using NLP techniques
- Exports results to CSV format for easy analysis
- Provides a clean, professional output suitable for news aggregation

## ✨ Features

- **🌐 Multi-site Support**: Works with Prothom Alo, Daily Star Bangla, and other major news sites
- **🧠 Smart Summarization**: Generates concise, readable summaries
- **🧹 Advanced Cleaning**: Removes ads, navigation elements, and "read more" links
- **📊 Export Options**: Saves results in CSV format with detailed metrics
- **🔧 Error Handling**: Robust error handling for network issues and file conflicts
- **📱 Professional Output**: Clean, properly formatted Bangla text

## 🛠️ Installation

### Prerequisites
- Python 3.11.9 (Recommended) or higher
- Internet connection for web scraping

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/news-summarizer.git
cd news-summarizer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup NLTK Data
```bash
python setup_nltk.py
```

## 📂 Project Structure

```
NewsSummarizer/
│
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── setup_nltk.py            # NLTK data setup script
├── bangla_stopwords.py      # Bangla stopwords database
├── news_scraper.py          # Main scraper and summarizer
└── summaries.csv            # Output file (generated after running)
```

## 🚀 Quick Start

### Method 1: Default Run (Recommended)
```bash
python news_scraper.py
```
This will automatically process pre-configured news articles and save results to `summaries.csv`.

### Method 2: Custom URLs
Edit the `bangla_news_urls` list in `news_scraper.py` to add your own news URLs:

```python
bangla_news_urls = [
    "https://www.prothomalo.com/your-news-url",
    "https://www.thedailystar.net/your-news-url",
    # Add more URLs here
]
```

## 📊 Output Format

The system generates a `summaries.csv` file with the following columns:

| Column | Description |
|--------|-------------|
| **Title** | News article headline |
| **URL** | Source article URL |
| **Source** | News website name |
| **Summary** | Generated summary (2-3 sentences) |
| **Original_Length** | Character count of original article |
| **Summary_Length** | Character count of summary |
| **Timestamp** | Processing date and time |

### Sample Output
```
Title: স্বাস্থ্য খাতে আলোচিত ঠিকাদার মিঠু পাঁচ দিন রিমান্ড
Source: Prothom Alo  
Summary: স্বাস্থ্য খাতে দুর্নীতির ঘটনায় আলোচিত ঠিকাদার মোতাজ্জেরুল ইসলাম ওরফে মিঠুকে পাঁচ দিন রিমান্ডে নিয়ে জিজ্ঞাসাবাদ করার অনুমতি দিয়েছেন আদালত। দুর্নীতি দমন কমিশনের একটি মামলায় সংস্থাটির আবেদনের পরিপ্রেক্ষিতে ঢাকা মহানগরের জ্যেষ্ঠ বিশেষ জজ সাব্বির ফয়েজ এ আদেশ দেন।
```

## ⚙️ Configuration

### Supported News Sites
- **Prothom Alo** (`prothomalo.com`)
- **The Daily Star** (`thedailystar.net`)
- **Generic Sites** (Most Bangla news websites)

### Customization Options

1. **Summary Length**: Modify the `sentences` parameter in `summarize_text()`:
```python
def summarize_text(self, text, sentences=2):  # Change to 3 or 4 for longer summaries
```

2. **Add New Stopwords**: Edit `bangla_stopwords.py` to add more filtering words.

3. **Custom News Sites**: Add site-specific scrapers in `news_scraper.py`.

## 📈 Performance Metrics

- **Processing Speed**: ~2-3 seconds per article
- **Compression Ratio**: 60-80% size reduction
- **Accuracy**: High-quality summaries with proper Bangla formatting

## 🔧 Troubleshooting

### Common Issues

**Issue**: `PermissionError` when saving CSV
```
Solution: Close Excel or any program that has the CSV file open
```

**Issue**: `ModuleNotFoundError` 
```bash
Solution: Run pip install -r requirements.txt
```

**Issue**: NLTK data missing
```bash
Solution: Run python setup_nltk.py
```

### Debug Mode
Add this at the beginning of `news_scraper.py` for detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🧪 Testing

Run with sample URLs to test functionality:
```bash
python news_scraper.py
```

Expected output:
- Console shows processing progress
- CSV file generated with summaries

## 📦 Dependencies

Core libraries used:
- `requests` - Web scraping
- `beautifulsoup4` - HTML parsing  
- `pandas` - Data manipulation
- `nltk` - Natural language processing
- `sumy` - Text summarization
- `flask` - Web framework (for future web interface)

## 🚀 Future Enhancements

- [ ] Web interface for easy URL input
- [ ] Real-time news feed integration
- [ ] Multiple language support
- [ ] Advanced AI summarization models

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📞 Support

For support and questions:
- 📧 Email: remonshahariar@gmail.com
- 📖 Documentation: This README file

## 🙏 Acknowledgments

- NLTK team for natural language processing tools
- Beautiful Soup for HTML parsing capabilities
- Sumy library for text summarization algorithms
- News websites for providing content

---

**⭐ Star this repository if you find it useful!**

**Made with ❤️ for automated news processing**
