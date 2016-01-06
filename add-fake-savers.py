# -*- encoding: utf-8 -*-
import string
from random import choice
from app.database import SuperSaver, create


for x in range(200):
    create(SuperSaver(
        ''.join([ choice(string.uppercase+string.digits) for x in range(6) ])
    ))
