import hashlib
import logging
import requests
from requests.exceptions import RequestException

from RESOURCES import RESOURCES
from utils.emailing import email_alert
from utils.checksum import get_checksum, create_checksum


def main():
    for RES in RESOURCES:
        try:
            res = requests.get(RES['url'])
            # hack, because some sites return 200 even when the resource is not found
            if res.headers['Content-Type'] != RES['mine']:
                raise RequestException
        except RequestException:
            logging.error(f"Request to {RES['ref']} failed. Failing url: {RES['url']}")
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
    logging.info('Started')
    main()
    logging.info('Ended successfully')
