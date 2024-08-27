import json
import logging
import os
from io import BytesIO
from typing import List, Optional
from urllib.parse import quote

import requests
from PIL import Image


class TelegramBot:
    def __init__(self, apikey: str, chat_id: str):
        """
        Initializes the TelegramBot instance.

        Args:
            apikey (str): The API key for accessing the Telegram bot.
            chat_id (str): The chat ID where the bot will send messages.
        """
        self.apikey = apikey
        self.chat_id = chat_id

    def send_media_group(
        self,
        images: List[str],
        caption: Optional[str],
        reply_to_message_id: Optional[int] = None,
    ) -> Optional[requests.Response]:
        """
        Sends a group of images as a media group to the Telegram chat.

        Args:
            images (List[str]): A list of image URLs to be sent.
            caption (Optional[str], optional): Caption to include with the first image. Defaults to None.
            reply_to_message_id (Optional[int], optional): ID of the message to reply to. Defaults to None.

        Returns:
            Optional[requests.Response]: The response object from the Telegram API if successful, None otherwise.
        """
        send_media_group_url = (
            f"https://api.telegram.org/bot{self.apikey}/sendMediaGroup"
        )
        files = {}
        media = []

        for i, img_url in enumerate(images):
            with BytesIO() as output:
                try:
                    response = requests.get(img_url, stream=True)
                    response.raise_for_status()
                    img = Image.open(response.raw)
                    img.save(output, format="PNG")
                    output.seek(0)
                    name = f"photo-{i}.png"
                    files[name] = output.read()
                    media.append({"type": "photo", "media": f"attach://{name}"})
                except Exception as e:
                    logging.error(f"Error processing image: {img_url}, Error: {e}")
                    continue

        if media:
            media[0]["caption"] = (
                caption if caption is not None else ""
            )  # Ensure caption is a string
            try:
                resp = requests.post(
                    send_media_group_url,
                    data={
                        "media": json.dumps(media),
                        "chat_id": self.chat_id,
                        "reply_to_message_id": reply_to_message_id,
                    },
                    files=files,
                )
                resp.raise_for_status()
            except requests.RequestException as e:
                logging.error(f"Error sending media group: {e}")
                resp = None
            finally:
                # Clean up temporary image files
                for img_name in files.keys():
                    try:
                        os.remove(img_name)
                    except OSError as remove_error:
                        logging.error(f"Error removing file {img_name}: {remove_error}")
            return resp
        else:
            logging.warning("No valid images to send in media group.")
            return None

    def send_simple_msg(self, msg: str) -> Optional[requests.Response]:
        """
        Sends a simple text message to the Telegram chat.

        Args:
            msg (str): The message text to send.

        Returns:
            Optional[requests.Response]: The response object from the Telegram API if successful, None otherwise.
        """
        room_desc_encoded = quote(msg.encode("utf8"))
        url = f"https://api.telegram.org/bot{self.apikey}/sendMessage?chat_id={self.chat_id}&text={room_desc_encoded}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Error sending simple message: {e}")
            return None
