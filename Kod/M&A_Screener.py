import yfinance as yf

list_of_tickers = ['ABB.ST', 'NOKIA.HE', 'NOVO-B.CO', 'EQNR.OL', 'NIBE-B.ST', 'GOMX.ST', 'KAMBI.ST', 'KJELL.ST', 'LUC.ST']

currency_to_ticker = {
    "USD": "USDSEK=X",
    "EUR": "EURSEK=X",
    "DKK": "DKKSEK=X",
    "NOK": "NOKSEK=X"
}

def get_rate_to_sek(currency):
    if currency == "SEK":
        return 1.0
    ticker = currency_to_ticker.get(currency)
    if ticker:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.fast_info.last_price
        return data
    return None


for ticker in list_of_tickers:
    ticker_obj = yf.Ticker(ticker)
    data = ticker_obj.info

    MarketCap = data.get('marketCap', 'N/A')
    MarketCapInSEK = MarketCap * get_rate_to_sek(data.get('currency', 'N/A')) if MarketCap != 'N/A' else None
  
    totalDebt = data.get('financialCurrency', 'N/A')
    totalDebtSEK = data.get('totalDebt', 'N/A') * get_rate_to_sek(data.get('financialCurrency', 'N/A')) if data.get('totalDebt', 'N/A') != 'N/A' else None

    totalCash = data.get('financialCurrency', 'N/A')
    totalCashSEK = data.get('totalCash', 'N/A') * get_rate_to_sek(data.get('financialCurrency', 'N/A')) if data.get('totalCash', 'N/A') != 'N/A' else None

    totalRevenue = data.get('financialCurrency', 'N/A')
    totalRevenueSEK = data.get('totalRevenue', 'N/A') * get_rate_to_sek(data.get('financialCurrency', 'N/A')) if data.get('totalRevenue', 'N/A') != 'N/A' else None

    evSEK = MarketCapInSEK + totalDebtSEK - totalCashSEK
    ebitdaSEK = data.get('ebitda', 'N/A') * get_rate_to_sek(data.get('financialCurrency', 'N/A')) if data.get('ebitda', 'N/A') != 'N/A' else None

    if evSEK is not None and ebitdaSEK is not None and ebitdaSEK != 0:
        evEbitda = evSEK / ebitdaSEK
    else:
        evEbitda = None

    trailingPEInSEK = data.get('trailingPE', 'N/A') if data.get('trailingPE', 'N/A') != 'N/A' else None

    print(f"Name: {data.get('shortName', 'N/A')}")
    print(f"Ticker: {ticker}")
    print(f"Country: {data.get('country', 'N/A')}")
    print(f"Sector: {data.get('sector', 'N/A')}")
    print(f"Trailing P/E: {trailingPEInSEK:.2f}" if trailingPEInSEK is not None else "Trailing P/E: N/A")
    print(f"EBITDA-margin: {((data.get('ebitdaMargins', 'N/A'))*100): .2f}%")
    print(f"EV/EBITDA: {evEbitda:.2f}" if evEbitda is not None else "EV/EBITDA: N/A")
    print(f"Market Cap: {MarketCapInSEK: .2f} in SEK converted from {data.get('currency', 'N/A')} \n")


