import random
from datetime import datetime


def new_id():
    return f"{random.randint(0, 999):03d}{datetime.now():%y%m%d%H%M%S}"
