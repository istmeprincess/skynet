import importlib
import re
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown

from skynet import dispatcher, updater, TOKEN, WEBHOOK, OWNER_ID, DONATION_LINK, CERT_PATH, PORT, URL, LOGGER \
    ALLOW_EXCL

from skynet.modules import ALL_MODULES
from skynet.modules.helper_funcs.chat_status import is_user_admin
from skynet.modules.helper_funcs.misc import paginate_modules

PM_START_TEXT = """
hello {}, my name is {}!!

i am a group manager bot helps you to keep your group safe and clean...

For more commands type - /help...

wishing you a very good day ahead!

"""

HELP_STRINGS = """

Hello there, my name is *{}*!

*Main* commands that are available:
- /start: Starts this skynet...
- /help: get more help!
- /donate: To get more info where to donate for better skynet's health!
- /settings:
  - in pm: To find out what SETTINGS you have set...
  - in a group: to setup your group...

{}
And the following:
""".format(dispatcher.bot.first_name, "" if not ALLOW_EXCL else "\nAll of the following commands / or ! can be used.... \n")

DONATE_STRING = """Heyaaaa,  glad to hear that you want to donate for this skynet!
It took lot of efforts & work for [my creator](https://gitlab.com/SinChanNohara) to get me where i am now!!! Every little donations helps \
motivate him to make me even better...."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
  imported_module = importlib.import_module("skynet.modules." + module_name)
  if not hasattr(imported_module, "__mod_name__"):
    imported_module.__mod_name__ = imported_module.__name__
    
  if not imported_module.__mod_name__.lower() in IMPORTED:
    IMPORTED[imported_module.__mod_name__.lower()] = imported_module
  else:
    raise Exception("Cant have two modules with the same name! Please change one of them")
    
  if hasattr(imported_module, "__help__") and imported_module.__help__:
    HELPABLE[imported_module.__mod_name__.lower()] = imported_module
    
  #Chat migration events:
  if hasattr(imported_module, "__migrate__"):
    MIGRATEABLE.append(imported_module)
    
  if hasattr(imported_module, "__stats__"):
    STATS.append(imported_module)
    
  if hasattr(imported_module, "__user_info__"):
    USER_INFO.append(imported_module)
    
  if hasattr(imported_module, "__import_data__"):
    DATA_IMPORT.append(imported_module)
    
  if hasattr(imported_module, "__export_data__"):
    DATA_EXPORT.append(imported_module)
    
  if hasattr(imported_module, "__chat_settings__"):
    CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module
    
  if hasattr(imported_module, "__user_settings__"):
    USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module
    
#no async
def send_help(chat_id, text, keyboard=None):
  if not keyboard:
    keyboard = InlinekeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
  dispatcher.bot.send_message(chat_id=chat_id,
                              text=text,
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=keyboard)
  
@run_async
def test(bot: Bot, update: Update):
  update.effective_message.reply_text("This person edited a message")
  print(update.effective_message)
  
@run_async
def start(bot: Bot, update: Update, args: List[str]):
  if update.effective_chat.type == "private":
    if len(args) >= 1:
      if args[0].lower() == "help":
        send_help(update.effective_chat.id, HELP_STRINGS)
        
      elif args[0].lower().startswith("stngs_"):
