import json
from collections import defaultdict
from datetime import datetime

with open('C:/Users/Harshit/Downloads/SaffronAi/transaction_detail.json') as f:
    data = json.load(f)

transactions = data['data'][0]['dtTransaction']

scheme_units = defaultdict(float)

def parse_date(date_str):
    return datetime.strptime(date_str, '%d-%b-%Y')

transactions.sort(key=lambda x: parse_date(x['postedDate']))

for txn in transactions:
    scheme = txn['scheme']
    trxn_units = float(txn['trxnUnits'])
    
    scheme_units[scheme] += trxn_units

for scheme, units in scheme_units.items():
    print(f"Scheme: {scheme}, Cumulative trxnUnits: {units}")
