import requests

from posting_app.database import Posting


class TelegramService:
    def __init__(
        self,
        bot_token: str,
        chat_room: str
    ):
        self._bot_token = bot_token
        self._chat_room = chat_room

    def format_posting_to_message(self, posting: Posting) -> str:
        '''Formats the object into a Telegram message.'''
        msg = '\n<a href="{}"> ‏ </a>\n<a href="{}"><b>{}</b></a>\n<i>{}</i>\n\n{}'.format(
            posting.location,   
            posting.url,
            posting.title,        
            posting.price,
            posting.description,
        )

        return msg
    
    def send_telegram_message(self, msg_text: str) -> bool:
        url = (
            'https://api.telegram.org/bot{}/'
            'sendMessage?chat_id={}&text={}&parse_mode=html'
        ).format(
            self._bot_token,
            self._chat_room,
            msg_text
        )
        res = requests.get(url)

        return res.ok