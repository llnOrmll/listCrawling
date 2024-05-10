# KRX Stock Data Scraper

Python script that scrapes stock data from the Korea Exchange (KRX) and generates a list of stocks based on trading volume and market capitalization.

## Project Structure

The project consists of three main files:

1. `main.py`: The main script that orchestrates the data retrieval and processing.
2. `krx_connector.py`: A module that provides a connection to the KRX API and retrieves stock price data.
3. `list_scraper.py`: A module that scrapes stock lists from the Naver Finance website based on trading volume and market capitalization.

## Dependencies

The project requires the following Python libraries:

- `google-cloud-bigquery`: For interacting with Google BigQuery.
- `requests`: For making HTTP requests to the KRX API and Naver Finance website.
- `beautifulsoup4`: For parsing HTML content.
- `pandas`: For data manipulation and analysis.

## Usage

1. Set up the necessary environment variables and configurations:
   - Provide the path to the Google Cloud service account credentials JSON file in `main.py`.
   - Modify the BigQuery table name in `main.py` to match your project and dataset.

2. Run the `main.py` script to execute the stock data scraping process.

3. The script will retrieve the last searched stock names from the BigQuery table and use them to filter out duplicate stocks.

4. It will then scrape the stock lists from Naver Finance based on trading volume and market capitalization.

5. The scraped data will be processed and saved as CSV files in the `dataset` directory:
   - `list_all.csv`: Contains the combined list of stocks from both trading volume and market capitalization.
   - `list_summary.csv`: Contains a summary of the top stocks in each category (KOSPI volume, KOSDAQ volume, KOSPI market cap, KOSDAQ market cap).

## Notes

- The `krx_connector.py` module uses the KRX API to retrieve stock price data. It constructs the necessary URLs and headers for making requests to the KRX API.

- The `list_scraper.py` module scrapes stock lists from the Naver Finance website. It uses the `requests` library to send HTTP requests and the `beautifulsoup4` library to parse the HTML content.

- The script incorporates a delay of 3 seconds between each request to the KRX API to avoid overloading the server.

- The script filters out stocks with names containing "인버스" (inverse) or "레버리지" (leverage) from the summary list.

## Disclaimer

Please note that this script is for educational and informational purposes only. Use it responsibly and in compliance with the terms of service of the respective websites and APIs. The author and contributors of this project are not responsible for any misuse or damage caused by the script.
