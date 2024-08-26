import json
import logging
from typing import Any, Dict, List, Optional

import requests
from db import create_table, sync_houses
from dotenv import dotenv_values
from scrape import house_to_msg, scrape
from telegram import TelegramBot

# Load environment variables
env = dotenv_values(".env")
TELEGRAM_API_KEY = env.get("TELEGRAM_API_KEY")
DEBUGGING_CHAT_ID = env.get("DEBUGGING_CHAT_ID")

# Initialize the debug Telegram bot
debug_telegram = TelegramBot(apikey=TELEGRAM_API_KEY, chat_id=DEBUGGING_CHAT_ID)


def read_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Reads the configuration from the specified JSON file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: Configuration data as a dictionary.
    """
    try:
        with open(config_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("Error reading configuration file: %s", e)
        debug_telegram.send_simple_msg(f"Error reading configuration file: {e}")
        raise


def process_house_notifications(
    telegram: TelegramBot, houses: List[Dict[str, Any]]
) -> None:
    """
    Processes and sends notifications for new houses.

    Args:
        telegram (TelegramBot): The Telegram bot instance used to send notifications.
        houses (List[Dict[str, Any]]): A list of dictionaries containing house data.
    """
    for h in houses:
        try:
            # Send house details as a simple message
            res: Optional[requests.Response] = telegram.send_simple_msg(house_to_msg(h))
            logging.info(
                "Sent Telegram notification for %s", h.get("url_key", "unknown")
            )

            # Check for unsuccessful send attempts
            if res and res.status_code != 200:
                error_msg = (
                    "Failed to send Telegram notification for %s: %s",
                    h.get("url_key", "unknown"),
                    res.json(),
                )
                debug_telegram.send_simple_msg(
                    f"Failed to send Telegram notification for {h.get('url_key', 'unknown')}: {res.json()}"
                )
                logging.error(*error_msg)

        except Exception as error:
            error_msg = (
                "Error sending notification for house %s: %s",
                h.get("url_key", "unknown"),
                error,
            )
            debug_telegram.send_simple_msg(
                f"Error sending notification for house {h.get('url_key', 'unknown')}: {error}"
            )
            logging.error(*error_msg)


def main() -> None:
    """
    Main function to scrape house data and send notifications via Telegram.
    """
    create_table()
    config = read_config("config.json")

    for group in config["telegram"]["groups"]:
        cities = group["cities"]
        chat_id = group["chat_id"]
        telegram = TelegramBot(apikey=TELEGRAM_API_KEY, chat_id=chat_id)

        # Scrape house data for the specified cities
        houses_in_cities = scrape(cities=cities)

        for city_id, houses in houses_in_cities.items():
            # Synchronize houses with the database and get new houses
            new_houses = sync_houses(city_id=city_id, houses=houses)

            # Process and send notifications for new houses
            process_house_notifications(telegram, new_houses)


if __name__ == "__main__":
    main()
