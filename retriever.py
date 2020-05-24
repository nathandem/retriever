import hashlib
import requests
from requests.exceptions import RequestException
from utils.emailing import email_alert
from utils.checksum import get_checksum, create_checksum


RESOURCES = [
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


for RES in RESOURCES:
    try:
        res = requests.get(RES['url'])
    except RequestException:
        print(f"Error while reaching out to {RES['ref']}")
        continue

    binary_content = res.content
    new_checksum = hashlib.md5(binary_content).hexdigest()

    recorded_checksum = None
    try:
        recorded_checksum = get_checksum(RES['ref'])
    except FileNotFoundError:
        create_checksum(ref=RES['ref'], checksum=new_checksum)
        email_alert(**RES)
    else:
        if new_checksum != recorded_checksum:
            create_checksum(ref=RES['ref'], checksum=new_checksum)
            email_alert(**RES)
            continue
        print(f"Today's checksum match recorded one for {RES['ref']}")
