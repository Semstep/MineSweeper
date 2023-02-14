FORM_BG_COLOR = (0, 0, .15)

TOP_BG_COLOR = (.1, .1, .1)
FIELD_BG_COLOR = (.3, .3, .3)
# FIELD_BG_COLOR = (.1, 1, 1)

LEVEL = 'amateur'

# Новичек: 8х8 10 мин (6.4), Любитель: 16х16 40 мин (6.4), Профи: 30х16 99мин (4.85).
LEVELS = {'newbie': (8, 8, 10), 'amateur': (16, 16, 4), 'profi': (30, 16, 99), '45': (4, 5, 5)}

FIELD_ROWNUM, FIELD_COLNUM, NUM_OF_MINES = LEVELS[LEVEL]

LOGFILE = r'logs/log.txt'