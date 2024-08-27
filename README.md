# 🏡 Holland2Stay Notifier

A simple bot that sends notifications about newly published houses on Holland2Stay to specific Telegram groups.

## 🚀 Installation

Follow these steps to set up the project:

1. **🔄 Clone the Repository:**
   ```bash
   git clone <repository-url>
   ```

2. **🐳 Start the .devcontainer**
```bash
ENV FILE
```
3. **📝 Copy and Update Configuration Files:**
   ```bash
   cp config_example.json config.json
   cp env_example .env
   ```
   - Update `config.json` and `.env` with your desired chat group and Telegram bot details.

4. **📦 Install Dependencies with Poetry:**
   Instead of using `requirements.txt`, this project uses [Poetry](https://python-poetry.org/) for dependency management. Install Poetry if you haven't already, and then install the dependencies:
   ```bash
   poetry install
   ```

5. **🔧 Run the Bot for Testing:**
   ```bash
   poetry run python main.py
   ```

## 🎥 Demo

Join the relevant Telegram group to see the bot in action. The bot posts new housing listings (with direct links removed to prevent spamming):

- **🏙️ The Hague, Amsterdam, Rotterdam, Zoetermeer, Capelle** -> [@h2notify](https://t.me/h2notify)
- **🏘️ Eindhoven, Helmond, Den Bosch, Tilburg** -> [@h2snotify_eindhoven](https://t.me/h2snotify_eindhoven)
- **🏡 Arnhem, Nijmegen** -> [@h2snotify_arnhem](https://t.me/h2snotify_arnhem)

## 🛠️ Usage

To automate the bot, add a cron job to run the project periodically. For example:

1. **📜 Create a Shell Script to Run the Bot (`run.sh`):**
   ```bash
   #!/bin/bash
   cd /home/user/projects/Holland2StayNotifier/h2snotifier/
   poetry run python main.py
   ```

2. **⏰ Add a Cron Job:**
   ```bash
   crontab -e
   ```
   Add the following line to run the script every 5 minutes:
   ```bash
   */5 * * * * cd /home/user/projects/Holland2StayNotifier/h2snotifier/ && bash ./run.sh
   ```

## 🔍 Pre-commit Hooks and Code Quality

This project uses [pre-commit](https://pre-commit.com/) and [pylint](https://pylint.pycqa.org/) to enforce code quality:

1. **🛡️ Set Up Pre-commit Hooks:**
   Install pre-commit and set up the hooks defined in `.pre-commit-config.yaml`:
   ```bash
   poetry run pre-commit install
   ```

2. **🧹 Run Pylint:**
   Ensure your code adheres to quality standards by running pylint:
   ```bash
   poetry run pylint <your-python-files>
   ```

## ⚙️ Continuous Integration (CI)

To maintain code quality and consistency, integrate the following checks into your CI pipeline:

1. **✅ Run Pre-commit Checks:**
   Ensure pre-commit hooks pass before merging any changes.

2. **🔍 Run Pylint:**
   Include pylint checks as part of your CI process to catch potential issues early.

## 👥 Contributors

[Your list of contributors here]
