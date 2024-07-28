# Visualization Techniques for Tracking Carbon Credit Trading Pathways and Identifying Potential Arbitrage Activities
> A method for visual analysis of token transaction data on the blockchain to quickly identify suspicious transactions.
## Installation Guide
Please follow the steps below to install and configure this project :

**STEP 1:** 
```
git clone https://github.com/Manchien/Tahrd-carbon.git
```

**STEP 2:** Setup virtual environment and install dependencies using `pip install -r requirements.txt`

**STEP 3:** Replace the credentials in the .env file with your own API_KEYS

## User Guide

[🎞️Video demonstration](https://youtu.be/iYVHpzPRlJo?si=DIIhOEPbh2lxF7YL):  Visualization Techniques for Tracking Carbon Credit Trading Pathways

Here are instructions on how to use this project.

### Data Collection： 

**Obtaining Multi-layer Historical Transaction Data for a Wallet:**
1. Copy the wallet address(es) you want to track and paste them into the INITIAL_ADDRESSES in the main function on line 84 of the file `data_collection.py.`

2. Modify the `MAX_DEPTH` parameter in the .env file according to the maximum number of layers you want to track.

3. Adjust the `TX_COUNT_THRESHOLD` in .env to set the number of transactions per layer you want to track ( Note: If no limit is set, the process may take several hours).

4. Run the script:
```
py data_collection.py
```
5. Obtain the CSV file.

**Obtaining Single-layer Historical Transaction Data for a Wallet:**
1. Directly download the transaction data from [Etherscan](https://etherscan.io/).

### Data Visualization：
1. Replace 'path/to/your/csvfile.csv' in the file_path variable with the path to your CSV file containing the transaction data. This can be found in the main function on line 7 of the file graph.py.
2. Run the application:
```
python graph.py
```
3. Open a web browser and navigate to the address in the command line (usually http://127.0.0.1:8050/) to view the dashboard.

### Examples of how to use the tool
> [What Addresses are Potential Fraud Accounts?](https://github.com/Manchien/Tahrd-carbon/blob/main/docs/example.pdf)
