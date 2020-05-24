**Retriever tracks files on the internet and notifies you when they are updated.**

Currently, I use it to let me know when new editions of some financial research papers that I follow are available. But it would work for anything else (text files, images, videos, etc).


## How to run?

#### Pre-requisite
Having a Mailjet account. If you prefer using another email provider, you can adjust that in ``utils/emailing.py``

#### Steps

1. Set-up a python virtual env (3.7 or above)
    ```bash
    python3 -m venv .venv

    source .venv/bin/activate
    ```

2. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `checksums` directory somewhere in the filesystem

4. Set the project environment variables

| Environment variable    | Description        | Required |
| ----------------------- | ------------------ | -------- |
| RETRIEVER_MJ_API_KEY    | Mailjet API key    | Yes       |
| RETRIEVER_MJ_API_SECRET | Mailjet API secret | Yes       |
| RETRIEVER_CHECKSUM_DIR_PATH | Path to the `checksums` directory (with a `/` at the end!) | Yes       |
| RETRIEVER_RECEIVER_EMAIL | Emails address where emails should be sent | Yes       |
| RETRIEVER_RECEIVER_NAME | Name of the receiver if any | No       |
| RETRIEVER_SENDER_EMAIL  | Email to use for the sender | Yes       |

You're done, you can now execute the script! 🎉

    python retriever.py


## How to run retriever frequently?

If you have a linux instance at your disposal, one way to run retriever regularly is to add a crontab entry (`crontab -e`).

If you want this script to run, say, every day at 8am, that would look something like:

	SHELL=/bin/bash
	MAILTO=""
	0 8 * * * (cd ~/retriever && . .venv/bin/activate && . .env && python retriever.py) >> ~/retriever/logs.txt 2>&1

where:
- ``SHELL=/bin/bash`` sets the shell to `bash`, a standard, more rich featured shell than `sh`
- ``MAILTO="""`` makes sure crontab doesn't try to send us emails. If we don't do that cron will try and it will likely fail because most linux instances don't have a STMP server configured by default.
- ``0 8 * * *`` is setting the frequency at which cronjob runs the command, i.e. every day of every month at 8 (A.M.)
- ``cd ~/retriever`` set the current directory of the bash session to the location of the project
- ``. .venv/bin/activate`` enters the python virtual environment
- ``. .env`` executes a shell script loading the environment variables
- ``python retriever.py`` calls the python interpreter to execute our program
- ``>> ~/retriever/logs.txt 2>&1`` tells bash to append the stout and sterr of all the preceding commands to `~/retriever/logs.txt` (and create the file is it doesn't exist)
