import yfinance as yf  # Import the yfinance library for downloading stock data

def get_rsi(data, period=14):
  """
  Calculates the Relative Strength Index (RSI) for a given stock data.

  Args:
    data: Pandas DataFrame containing historical stock data.
    period: Number of periods used for RSI calculation.
  """
  delta = data['Close'].diff()  # Calculate the price change for each period
  gain = (delta.where(delta > 0, 0)).fillna(0)  # Calculate gains (positive price changes)
  loss = (-delta.where(delta < 0, 0)).fillna(0)  # Calculate losses (negative price changes)
  avg_gain = gain.rolling(window=period).mean()  # Calculate average gain over the specified period
  avg_loss = loss.rolling(window=period).mean()  # Calculate average loss over the specified period
  rs = avg_gain / avg_loss  # Calculate Relative Strength (RS)
  rsi = 100 - (100 / (1 + rs))  # Calculate RSI using the formula
  return rsi

def get_stock_data(ticker):
  """
  Fetches historical stock data for the given ticker symbol using yfinance.
  """
  data = yf.download(ticker)  # Download stock data from Yahoo Finance
  return data

def check_alerts(data, buy_price_range, sell_price_range, stop_loss):
  """
  Checks for buy/sell signals based on price and RSI conditions.
  """
  rsi = get_rsi(data)  # Calculate RSI for the stock data

  # Define price and RSI conditions
  buy_signal = (data['Close'] >= buy_price_range[0]) & (data['Close'] <= buy_price_range[1])
  sell_signal = (data['Close'] >= sell_price_range[0]) & (data['Close'] <= sell_price_range[1])
  oversold_signal = rsi < 30
  overbought_signal = rsi > 80

  # Calculate stop-loss price
  stop_loss_price = data['Close'] * (1 - stop_loss / 100)

  alerts = []  # Initialize an empty list to store alerts

  for i in range(len(data)):
    if buy_signal[i] and oversold_signal[i]:  # If both buy price and oversold conditions are met
      alerts.append(("Buy", data.index[i], data['Close'][i], stop_loss_price[i]))
    elif sell_signal[i] and overbought_signal[i]:  # If both sell price and overbought conditions are met
      alerts.append(("Sell", data.index[i], data['Close'][i], stop_loss_price[i]))
    else:  # If no conditions are met
      alerts.append(("No Signal", data.index[i], data['Close'][i], None))

  return alerts

if __name__ == "__main__":
  ticker = "AAPL"  # Stock ticker symbol
  buy_price_range = (100, 110)  # Buy price range
  sell_price_range = (150, 160)  # Sell price range
  stop_loss = 10  # Stop-loss percentage

  data = get_stock_data(ticker)  # Get stock data
  alerts = check_alerts(data, buy_price_range, sell_price_range, stop_loss)  # Generate alerts

  for alert in alerts:
    print(f"{alert[0]} Signal at {alert[1]}: Price: {alert[2]} | Stop-Loss: {alert[3]}")
