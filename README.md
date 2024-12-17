# Visualization and Data Collection Tool for Blockchain Transactions

## Overview

This project includes two main Python scripts:

1. data_collection.py: This script collects multi-layer Ethereum transaction data for specific wallets using the Etherscan API and exports the results to a CSV file.
2. graph.py: Provides an interactive web-based dashboard to visualize the collected blockchain transactions as a network graph.

The tool tracks carbon credit trading pathways and identifies potential arbitrage or suspicious activities.

## Features

Data Collection (data_collection.py):

1. Collects wallet-to-wallet transaction data recursively up to a defined depth.
2. Filters transactions to remove duplicates and zero-value transfers.
3. Outputs data in a structured CSV format for visualization.

Data Visualization (graph.py):

1. Visualizes transaction relationships as an interactive graph.
2. Allows filtering by time range and transaction layers.
3. Highlights the top 10 most significant transactions and high-frequency wallets.
4. Provides detailed insights for selected nodes and edges.

## Installation Guide
STEP 1: Clone the Repository

    git clone https://github.com/peculab/TrackingCarbon.git
    cd TrackingCarbon

STEP 2: Set Up the Virtual Environment and Install Dependencies

    python -m venv venv
    source venv/bin/activate  # For MacOS/Linux
    venv\Scripts\activate     # For Windows
    pip install -r requirements.txt

STEP 3: Configure the Environment

Create a .env file in the root directory and add the following:

    ETHERSCAN_API_KEY=your_etherscan_api_key
    MAX_DEPTH=3
    TX_COUNT_THRESHOLD=10
-  ETHERSCAN_API_KEY: Your API key for the Etherscan API.
-  MAX_DEPTH: Maximum recursive wallet depth to track.
-  TX_COUNT_THRESHOLD: Maximum number of transactions per wallet to process.

## User Guide
Data Collection with data_collection.py

1. Open data_collection.py and replace the placeholder wallet addresses in the INITIAL_ADDRESSES list (line 51):

        INITIAL_ADDRESSES = ['0xYourWalletAddressHere']

2. Run the script:

        python data_collection.py

3. The resulting transaction data will be saved as result.csv in the data/ folder.

Visualize Data with graph.py

1. Open graph.py and set the path to your CSV file (line 5):

        file_path = 'data/result.csv'

2. Run the visualization tool:

        python graph.py

3. Open a browser and navigate to:

        http://127.0.0.1:8050/

4. Dashboard Features:
   - Time Range Filter: Select a time range for transactions.
   - Layer Range Slider: Filter transactions by wallet depth (layer).
   - Top 10 Transactions: Highlight the most significant transactions.
   - High-Frequency Nodes: Highlight wallets with more than five transactions daily.
   - Node Details: Click on a node to view its total value, degree, and transaction history.
   - Edge Details: Click on an edge to view the transaction count and value.

## Workflow

1. Use data_collection.py to collect multi-layer wallet transaction data and save it as a CSV file.
2. Use graph.py to load and visualize the data interactively.

## Example Use Case

1. Tracking Carbon Credit Transactions: Track wallet transactions interacting with the MCO2 token to analyze carbon credit pathways.
2. Identifying Arbitrage or Fraud: Use the graph visualization to detect wallets with abnormal transaction frequencies or large token movements.

## Notes

- Ensure your Etherscan API key has sufficient rate limits to support large data retrieval tasks.
- For deeper analysis, you can increase MAX_DEPTH or TX_COUNT_THRESHOLD, but be careful about API rate limits.
- Modify the process_transactions function in data_collection.py to include other token types or additional filtering logic.

## Project Structure

```plaintext
TrackingCarbon/
│
├── data_collection.py   # Data collection script
├── graph.py             # Visualization script
├── requirements.txt     # List of dependencies
├── .env                 # API configuration
├── data/                # Directory for storing CSV outputs
└── README.md            # Project documentation
```

## Dependencies

    Python 3.8+
    aiohttp
    pandas
    dash
    dash-cytoscape
    python-dotenv

Install dependencies using:

    pip install -r requirements.txt

## License

This project is licensed under the MIT License.

## Contact

For issues or questions, please contact the repository maintainer via GitHub.
