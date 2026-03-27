# NER Tagger — Production-Grade NLP Web Application

A professional, local-first Named Entity Recognition (NER) and Part-of-Speech (POS) tagging tool. Built with **spaCy** for advanced natural language understanding and **Flask** for a robust, lightweight backend.

![NER Tagger UI](file:///C:/Users/Aldrin%20Joan/.gemini/antigravity/brain/58ac2bae-fc18-4dcd-8ee9-77f4ba39d44b/analysis_results_1774583839879.png)

## 🚀 Features

- **Advanced Named Entity Recognition**: Automated extraction and categorization of Persons, Organisations, Locations, and Dates.
- **POS & Dependency Mapping**: Detailed token-level analysis including parts-of-speech and grammatical dependencies.
- **Premium Dark Mode UI**: A responsive, glassmorphic interface with micro-animations and smooth transitions.
- **Zero-Trust Input Validation**: Hardened backend with input sanitization and length limits to prevent DoS.
- **Local-First & Private**: Runs entirely on your local machine. No external APIs, no data leaks.
- **High Performance**: Optimized for Python 3.13 using the `waitress` production-ready server.

## 🛠️ Tech Stack

- **NLP Engine**: spaCy 3.8.x (`en_core_web_sm` model)
- **Backend**: Flask 3.1.x, Pandas 3.0.x
- **Frontend**: Vanilla CSS (Variables, Grid, Flexbox), JavaScript (Fetch API)
- **Server**: Waitress (Production WSGI)
- **Quality**: Pytest (Unit & Integration tests)

## 📦 Installation

### Prerequisites
- Python 3.10 to 3.13+
- pip (latest version recommended)

### Setup
1. **Clone the repository** (if applicable) or navigate to the project folder:
   ```bash
   cd ner-tagger
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies and download the spaCy model**:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

## 🖥️ Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the Web UI**:
   Open your browser and navigate to: [http://localhost:5000](http://localhost:5000)

3. **Analyze Text**:
   Paste any news article or paragraph into the input area and press `Analyse` (or `Ctrl+Enter`).

## 🧪 Testing & Quality Assurance

The project includes a comprehensive test suite covering core NLP logic and API endpoints.

```bash
# Run all tests
venv\Scripts\python -m pytest -v tests/
```

## 📂 Project Structure

```text
ner-tagger/
├── app.py             # Hardened Flask server & API routes
├── ner_engine.py      # Refactored NLP processing module
├── requirements.txt   # Pinned dependency manifest
├── static/            # Static assets
│   ├── script.js      # Frontend logic & XSS protection
│   └── style.css      # Premium UI styling
├── templates/         # UI templates
│   └── index.html     # Main application template
└── tests/             # Verification suite
    ├── test_app.py    # Integration tests
    └── test_engine.py # Unit tests
```

---
*Created with focus on Security, Performance, and Architectural Excellence.*
