# 📈 Stock Market Analysis with Technical Indicators + News

This Streamlit app allows you to analyze stock market data with technical indicators (Bollinger Bands, RSI, MACD) and view the latest news for any stock symbol. It features an easy-to-use dropdown for popular tickers, a custom symbol option, and a built-in feedback form.

## Features
- **Select stock symbol** from a dropdown of popular tickers or enter your own.
- **Interactive charts** for price, Bollinger Bands, RSI, and MACD.
- **Latest news** headlines for the selected stock.
- **Feedback form** for user suggestions and comments.

## How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/stock-market-app.git
   cd stock-market-app
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app**
   ```bash
   streamlit run app.py
   ```
4. Open the provided local URL in your browser.

## How to Deploy (Streamlit Community Cloud)
1. Push your code to a public GitHub repository.
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) and sign in with GitHub.
3. Click "New app", select your repo and branch, and set the main file to `app.py`.
4. Click "Deploy". Share the public URL with others!

## Feedback
- Use the built-in feedback form at the bottom of the app.
- Or fill out our [Google Form](https://forms.gle/your-google-form-link) for more detailed feedback.

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies.

## File Structure
```
app.py              # Main Streamlit app
requirements.txt    # Python dependencies
utils.py            # (Optional) Utility functions
```

## Customization
- Add more popular tickers to the dropdown in `app.py`.
- Replace the Google Form link with your own for structured feedback.

## License
MIT License

---

*Made with ❤️ using Streamlit, yfinance, pandas, and ta.*
