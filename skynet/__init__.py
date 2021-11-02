import logging
import os
import sys

import telegram.ext as tg

# enabling logging
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6 stop the bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
  LOGGER.error("You must have a python version of atleast 3.6!! Multiple feature depends upon this.. BOT DIES.")
  quit(1)
  
ENV = bool(os.environ.get('ENV', False))

if ENV:
  TOKEN = os.environ.get('TOKEN', None)
  try:
    OWNER_ID = int(os.environ.get('OWNER_ID', None))
  except ValueError:
    raise Exception("Your OWNER_ID env var is not valid integer")
    
  MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP', None)
  OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None))
  
  try:
    SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
  except ValueError:
    raise Exception("Your sudo user list doesnt seem to be valid...")
    
  try:
    SUPPORT_USERS = set(int(x) for x in os.environ.get("SUPPORT_USERS", "").split())
  except ValueError:
    raise Exception("Your support user list doesnt seems to be valid...")
    
  try:
    WHITELIST_USERS = set(int(x) for x in os.environ.get("WHITELIST_USERS", "").split())
  except ValueError:
    raise Exception("Your whitelisted user list doesnt seems to be valid...")
    
  WEBHOOK = bool(os.environ.get('WEBHOOK', False))
  URL = os.environ.get('URL', "") #It dont contains tokens
  PORT = int(os.environ.get('PORT', 5000))
  CERT_PATH = os.environ.get("CERT_PATH")
  
  DB_URI = os.environ.get('DATABASE_URL')
  DONATION_LINK = os.environ.get('DONATION_LINK')
  LOAD = os.environ.get("LOAD", "").split()
  NO_LOAD = os.environ.get("NO_LOAD", "").split()
  DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
  STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
  WORKERS = int(os.environ.get('WORKERS', 8))
  BAN_STICKER = os.environ.get('BAN_STICKER', '')
  ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False))
  STRICT_GMUTE = bool(os.environ.get('STRICT_GMUTE', False))
  
else:
  from skynet.config import Development as Config
  TOKEN = Config.API_KEY
  try:
    OWNER_ID = int(Config.OWNER_ID)
  except ValueError:
    raise Exception("Your OWNER_ID isnt valid...")
    
  MESSAGE_DUMP = Config.MESSAGE_DUMP
  OWNER_USERNAME = Config.OWNER_USERNAME
  
  try:
    SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
  except ValueError:
    raise Exception("Your sudo users list isnt valid...")
    
  try:
    WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
  except ValueError:
    raise Exception("Your whitelisted users list isnt valid...")
  
  try:
    SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
  except ValueError:
    raise Exception("Your support users list isnt valid...")
  
  WEBHOOK = Config.WEBHOOK
  URL = Config.URL
  PORT = Config.PORT
  CERT_PATH = Config.CERT_PATH
  
  DB_URI = Config.SQLALCHEMY_DATABASE_URI
  DONATION_LINK = Config.DONATION_LINK
  LOAD = Config.LOAD
  NO_LOAD = Config.NO_LOAD
  DEL_CMDS = Config.DEL_CMDS
  STRICT_GBAN = Config.STRICT_GBAN
  WORKERS = Config.WORKERS
  BAN_STICKER = Config.BAN_STICKER
  ALLOW_EXCL = Config.ALLOW_EXCL
  STRICT_GMUTE = Config.STRICT_GMUTE
  
SUDO_USERS.add(OWNER_ID)

updater = tg.Updater(TOKEN, workers=WORKERS)

dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

from skynet.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler

tg.RegexHandler = CustomRegexHandler

if ALLOW_EXCL:
  tg.CommandHandler = CustomCommandHandler
