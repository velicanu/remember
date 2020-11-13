# remember

## Requirements

- python3, < 3.9 (numpy currently broken on 3.9)
- node
- google api set up for speech recognition
  - ex: ENV variable `GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json`
- access to an Elasticsearch cluster

## Installation

git clone this repo then inside it:
```bash
pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ..
streamlit run app.py
```
