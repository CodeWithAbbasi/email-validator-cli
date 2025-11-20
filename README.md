# email-validator-cli
# Multithreaded Email Existence Checker (ODS + CLI)

A high-performance, **multithreaded email validator** for bulk ODS email lists.

- Checks MX records and SMTP existence
- Multithreaded for speed
- CLI with progress bar
- Outputs results back into `.ods` file

## Features

- Parallel email validation using ThreadPoolExecutor
- Progress bar with `tqdm`
- Configurable number of threads
- Handles corporate & freemail domains
- Enterprise-ready for large datasets

## Usage

```bash
python email_checker_cli.py -i emails.ods -o validated.ods -c email -t 20
