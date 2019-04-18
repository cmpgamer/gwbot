import json
from gw2api import Gw2API
from database import database as db
from psycopg2.extras import Json

with open('./database/db_settings.json') as json_file:
    config_data = json.load(json_file)['PostgresDatabase']



