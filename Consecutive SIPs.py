import json
from collections import defaultdict
from datetime import datetime, timedelta

with open('C:/Users/Harshit/Downloads/SaffronAi/transaction_detail.json') as file:
    data = json.load(file)

def extract_month_year(date_str):
    date = datetime.strptime(date_str, '%d-%b-%Y')
    return date.year, date.month

sip_transactions = [
    txn for txn in data['data'][0]['dtTransaction']
    if 'SIP' in txn['trxnDesc'].upper() or 'Systematic' in txn['trxnDesc'].upper()
]
transactions_by_scheme = defaultdict(list)

for txn in sip_transactions:
    scheme = txn['scheme']
    date = datetime.strptime(txn['trxnDate'], '%d-%b-%Y')
    transactions_by_scheme[scheme].append(date)

missing_sips = defaultdict(list)

for scheme, dates in transactions_by_scheme.items():
  
    dates.sort()
    
    start_date = dates[0].replace(day=1)  
    end_date = dates[-1].replace(day=1)  

    all_months = set()
    current_date = start_date

    while current_date <= end_date:
        all_months.add((current_date.year, current_date.month))
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)

    sip_months = set((date.year, date.month) for date in dates)

    missing_months = all_months - sip_months
    if missing_months:
        missing_sips[scheme] = sorted(missing_months)

for scheme, months in missing_sips.items():
    if months:
        missing_months_str = ', '.join([datetime(year, month, 1).strftime('%b-%Y') for year, month in months])
        print(f"Scheme: {scheme}, Missing SIPs: {missing_months_str}")
    else:
        print(f"Scheme: {scheme}, No missing SIPs.")
