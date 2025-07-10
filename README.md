# 📈 NextTrade - Stock Qualifier (Proprietary)

NextTrade is a powerful and private Streamlit-based stock analysis tool developed for bullish swing trading in NSE stocks. It allows users to filter and visualize the best trading candidates using a combination of technical indicators, volume spikes, and real-time corporate data such as earnings and dividend dates.

> 🔐 **This software is proprietary. Unauthorized use is strictly prohibited.**

---

## 🔧 Features

- 📊 Analyze a user-defined number of top NSE500 stocks
- ✅ Apply bullish screening conditions:
  - RSI between 55 and 65
  - MACD Histogram > 0 and MACD Line > Signal
  - Volume spike on up-day
  - 20 > 50 > 200 SMA structure
  - Price above 20/50/200 SMA
- 📈 Real-time interactive candlestick chart with SMA overlays
- 🗓️ Fetch upcoming earnings & dividend dates from Yahoo Finance
- 💾 Download filtered results as a CSV

---

## 🚀 How to Run Locally

### 1. Clone the Repository *(Private Access Only)*
```bash
git clone <your-private-repo-url>
cd nexttrade
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your Stock List
Create a file named `nse500.csv` in the root directory. It should have a column `Stock_Code` with the ticker codes (without `.NS`).

**Example `nse500.csv`:**
```csv
Stock_Code
RELIANCE
TCS
HDFCBANK
INFY
```

## 📂 Project Structure

```
nexttrade/
├── app.py              # Main Streamlit application
├── nse500.csv          # Your NSE500 stock list
├── requirements.txt    # Python dependencies
└── README.md           # This documentation
```

---

## 🔒 License & Terms

- This software is proprietary and developed by **Saksham Singla**.
- Redistribution, commercial use, or modification without written consent is strictly prohibited.
- For licensing queries or to request a key, please contact the developer.

---

© 2025 Saksham Singla. All rights reserved.
