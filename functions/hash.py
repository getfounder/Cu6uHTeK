# -*- coding: cp1251 -*-
from hashlib import sha256

def compute(msg):
    return sha256(msg.encode('cp1251')).hexdigest() == 'b15b171bb0f1e092f2fabf20386a0ecb034503b39983dd10fa30ff00a9564503'

