# CCX Backup

Quick application to backup Scripts, Prompts, and Documents from a Cisco UCCX Server. This has been developed and tested against UCCX 12.5SU1 in the Cisco DevNet Sandbox

## Setup

1. Create a new Python Virtual Environment with `python -m venv <venv-name>`
2. Activate the virtual environment with `source <venv-name>/bin/activate`
3. install required libraries in your new vitual enviroment with `pip install -r requirements.txt`

## Run

1. If not already activated, activate your virtual environment, if you do not have a virtual environment setup see the setup steps above
2. Run `python ccx_backup.py -h` to see a list of command line arguments and usage details
3. To run with minimum required arguments, run as `python ccx_backup.py -u <username> -p <password> -ip <ip address>` this will backup all prompts, scripts and documents

## Todo

Features / Enhancements to add sometime maybe

- async support for better speed (opted to stat wiithout to avoid hammering server)
- add progress bar to download so you can tell something is happening
- add alternative ways to input data (environmental variables or file, or just interactive prompts) so password dosn't show in cli history
  - add option through input file to backup multpile servers in one run
- add error handling
- refactor request gets, only a couple lines of code but it is repeated twice ... DRY
- don't ignore SSL certificate warnings by default, add a flag to allow user to determine if ignored
- improve documentation
- review how and when folders are created
