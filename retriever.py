import hashlib
import logging
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


def main():
    for RES in RESOURCES:
        try:
            res = requests.get(RES['url'])
        except RequestException:
            logging.error(f"Error while reaching out to {RES['ref']}")
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
            logging.info(f"Today's checksum match recorded one for {RES['ref']}")


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',  # iso8601 format
        level=logging.INFO,
    )
    logging.info('Start')
    main()
    logging.info('End')
