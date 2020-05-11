import hashlib
import requests
from requests.exceptions import RequestException
from utils.emailing import send_paper
from utils.checksum import get_checksum, create_checksum


PAPERS = [
    {
        'ref': 'NBC_MONTHLY_ECONOMIC',
        'name': 'National bank monthly economic monitor',
        'url': 'https://www.nbc.ca/content/dam/bnc/en/rates-and-analysis/economic-analysis/monthly-economic-monitor.pdf',
    },
    {
        'ref': 'NBC_MONTHLY_EQUITY',
        'name': 'National bank monthly equity monitor',
        'url': 'https://www.nbc.ca/content/dam/bnc/en/rates-and-analysis/economic-analysis/monthly-equity-monitor.pdf',
    },
    {
        'ref': 'NBC_MONTHLY_FIXED_INCOME',
        'name': 'National bank monthly fixed income monitor',
        'url': 'https://www.nbc.ca/content/dam/bnc/en/rates-and-analysis/economic-analysis/monthly-fixed-income-monitor.pdf',
    },
    {
        'ref': 'NBC_MONTHLY_FOREX',
        'name': 'National bank monthly economic monitor',
        'url': 'https://www.nbc.ca/content/dam/bnc/en/rates-and-analysis/economic-analysis/forex.pdf',
    },
]


for PAPER in PAPERS:
    try:
        res = requests.get(PAPER['url'])
    except RequestException:
        print(f"Error while reaching out to {PAPER['ref']}")
        continue

    binary_content = res.content
    new_checksum = hashlib.md5(binary_content).hexdigest()

    recorded_checksum = None
    try:
        recorded_checksum = get_checksum(PAPER['ref'])
    except FileNotFoundError:
        create_checksum(ref=PAPER['ref'], checksum=new_checksum)
        send_paper(**PAPER)
    else:
        if new_checksum != recorded_checksum:
            create_checksum(ref=PAPER['ref'], checksum=new_checksum)
            send_paper(**PAPER)
            continue
        print(f"Today's checksum match recorded one for {PAPER['ref']}")
