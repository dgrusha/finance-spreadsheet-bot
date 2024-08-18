# finance-spreadsheet-bot | @sheetfin_bot | Spreadsheet Finance

## Env information
* Python version 3.10.9
* MongoDB
* Redis
* Venv used

## Python env setup

### Save packages
```
pip freeze > requirements.txt
```

### Install packages
```
pip install -r requirements.txt
```

### Start in production mode
```
python main.py --type_of_env prod
```

### Start development mode
```
python main.py --type_of_env dev
```
OR
```
python main.py
```

## Pre-commit

### Install pre-commit to env
```
pip install pre-commit
```

### Install pre-commit to .git
```
pre-commit install
```

### Run all hooks from console
```
pre-commit run --all-files
```

## Commands available

* start - Start your work with this bot.
* description - Description of what this bot can do.
* enter_email - Enter your email, that will be needed to manage the spreadsheet.
* get_active_email - Get info on what email you have currently saved in this bot.
