import logging
import os


CHECKSUM_DIR_PATH = os.environ['RETRIEVER_CHECKSUM_DIR_PATH']


def get_checksum(ref: str) -> str:
    with open(f'{CHECKSUM_DIR_PATH}{ref}') as f:
        return f.read()


def create_checksum(ref: str, checksum: str):
    with open(f'{CHECKSUM_DIR_PATH}{ref}', 'w') as f:
        f.write(checksum)
        logging.debug(f"Created new checksum file for {ref}")
