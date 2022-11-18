# CCX Backup

Application to backup Scripts, Prompts, and Documents from a Cisco UCCX Server

## Setup

1. Create a new Python Virtual Environment with `python -m venv <venv-name>`
2. Activate the virtual environment with `source <venv-name>/bin/activate`
3. install required libraries in your new vitual enviroment with `pip install -r requirements.txt`

## Run

1. If not already activated, activate your virtual environment, if you do not have a virtual environment setup see the setup steps above
2. Run `python ccx_backup.py -h` to see a list of command line arguments and usage details
3. To run with minimum required arguments, run as `python ccx_backup.py -u <username> -p <password> -ip <ip address>` this will backup all prompts, scripts and documents
