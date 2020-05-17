Retriever tracks files on the internet and notifies you when they are updated.

Currently, I use it to notify me when new editions of some financial research papers that I follow are available. But it would work for anything else (text files, images, videos, etc).


How to install?
---------------

1. Set-up a python virtual env (3.7 or above)
    ```bash
    python3 -m venv .env

    source .env/bin/activate
    ```

2. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `checksums` directory somewhere in the filesystem. Load this path in the environment variable ``RETRIEVER_CHECKSUM_DIR_PATH``

4. Set the environment variables ``RETRIEVER_MJ_API_KEY`` and ``RETRIEVER_MJ_API_SECRET`` with your Mailjet credentials

You're done, you can now execute the script!

    python retriever.py


How to run retriever frequently?
--------------------------------

If you want this script to run say every day at 8am. You can add a crontab entry that would look something like:

	SHELL=/bin/bash
	0 8 * * * (cd ~/retriever && . .env/bin/activate && . project_env_var && python retriever.py) >> ~/dev/null 2>&1
