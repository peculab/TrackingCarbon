import asyncio
import os
import pandas as pd
import datetime
from dotenv import load_dotenv
import aiohttp

load_dotenv()
API_KEY = os.getenv('ETHERSCAN_API_KEY')  # Etherscan API Key

async def get_transactions(session, address, api_key):
    url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock=0&endblock=999999999&sort=asc&apikey={api_key}'
    async with session.get(url) as response:
        try:
            data = await response.json()
            return data['result']
        except:
            print(f"Error in getting transactions for address {address}")
            return []
        
def convert_timestamp_to_readable(time_stamp):
    dt_object = datetime.datetime.utcfromtimestamp(int(time_stamp))
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

def is_duplicate_event(new_event, existing_events):
    for event in existing_events:
        if all(new_event[key] == event[key] for key in new_event if key != 'layer'):
            return True
    return False

async def process_transactions(session, address, api_key, depth, max_depth, collected_data):
    if depth >= max_depth:
        return collected_data

    transactions = await get_transactions(session, address, api_key)
    tx_count = 0

    for tx in transactions:
        try:
            if tx['to'] == "0x0000000000000000000000000000000000000000":
                continue
            token_decimal = int(tx['tokenDecimal']) if tx['tokenDecimal'] else 0
            amount = int(tx['value']) / (10 ** token_decimal)
            readable_time = convert_timestamp_to_readable(tx['timeStamp'])
            if (amount != 0 and depth == 0 and tx['tokenSymbol'] == 'MCO2' ) or (tx['from'] == address and amount != 0 and depth > 0):
                event_data = {
                    'layer': depth,
                    'BlockNumber': tx['blockNumber'],
                    'TimeStamp': readable_time,
                    'Hash': tx['hash'],
                    'From': tx['from'],
                    'To': tx['to'],
                    'Value': amount,
                    'TokenName':tx['tokenName'],
                    'TokenSymbol':tx['tokenSymbol']
                }
            else:
                continue
            if is_duplicate_event(event_data, collected_data):
                continue
            if tx_count >= int(os.getenv('TX_COUNT_THRESHOLD')):
                break
            collected_data.append(event_data)
            print("event_data:", event_data)
            tx_count += 1
            await process_transactions(session, tx['to'], api_key, depth + 1, max_depth, collected_data)
        except Exception as e:
            print(f"Error in transaction {tx['hash']}: {e}")
            continue

    return collected_data

def save_to_csv(data, filename='result.csv'):
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(os.path.join('data', filename), index=False)
    print(f'CSV file {filename} has been saved.')

async def main():
    async with aiohttp.ClientSession() as session:
        collected_data = []
        depth = 0
        max_depth = int(os.getenv('MAX_DEPTH'))
        INITIAL_ADDRESSES = [
            'The wallet address you want to track'
        ]
        tasks = [process_transactions(session, address, API_KEY, depth, max_depth, collected_data) for address in INITIAL_ADDRESSES]
        await asyncio.gather(*tasks)
        save_to_csv(collected_data)

if __name__ == "__main__":
    asyncio.run(main())