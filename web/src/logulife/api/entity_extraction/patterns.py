'''Паттерны для извлечения сущностей'''

P_SPACE = r'[ \n\t]'
P_ANY = r'(.+)'

# Числа
P_NUMBER = r'([0-9]+)((\.|,)[0-9]+)?'
P_LETTER_NUMBER = r'({number})(k|к)'.format(number=P_NUMBER)

# Показатели времени
P_HOUR = r'час(а|ам|ами|ах|е|ов|ом|у|ы)?'
P_MINUTE = r'минут(а|ам|ами|ах|е|ой|у|ы)?'
P_SECOND = r'секунд(а|ам|ами|ах|е|ой|у|ы)?'
P_HALF_HOUR = r'полчас(а|ам|ами|ах|е|ой|у|ы)?'
P_HOUR_AND_HALF = r'полтор(а|ы){space}{hour}'.format(space=P_SPACE, hour=P_HOUR)

# Показатели даты
P_TODAY = r'сегодня'
P_YESTERDAY = r'вчера'
P_TOMORROW = r'завтра'

# Времена года
P_AUGUST = r'август(а|ам|ами|ах|е|ов|ом|у|ы)?'
P_APRIL = r'апрел(е|ей|ем|и|ь|ю|я|ям|ями|ях)'
P_DECEMBER = r'декабр(ь|и|я|ей|ю|ям|ём|ями|е|ях)'
P_JULY = r'июл(ь|и|я|ей|ю|ям|ем|ями|е|ях)'
P_JUNE = r'июн(ь|и|я|ей|ю|ям|ем|ями|е|ях)'
P_MAY = r'ма(й|и|я|ев|ю|ям|ем|ями|е|ях)'
P_MARCH = r'март(ы|а|ов|у|ам|ом|ами|е|ах)?'
P_NOVEMBER = r'ноябр(ь|и|я|ей|ю|ям|ём|ями|е|ях)'
P_OCTOBER = r'октябр(ь|и|я|ей|ю|ям|ём|ями|е|ях)'
P_SEPTEMBER = r'сентябр(ь|и|я|ей|ю|ям|ём|ями|е|ях)'
P_FEBRUARY = r'феврал(ь|и|я|ей|ю|ям|ём|ями|е|ях)'
P_JANUARY = r'январ(ь|и|я|ей|ю|ям|ём|ями|е|ях)'

# Показатель веса
P_WEIGHT = r'ве(с|са|сов|су|сам|сом|сами|се|сах|сить|шу)'

# Валюты
P_RUB = r'(рубл(ями|ям|ях|ей|ём|е|и|ь|ю|я)|₽)'
P_USD = r'(доллар(ами|ов|ом|ам|ах|а|е|у|ы)?|бакс(ами|ам|ах|ов|ом|а|е|у|ы)?|\$)'
P_EUR = r'(евро|€)'
P_VND = r'(дон(гами|гам|гах|гов|гом|га|ге|ги|гу|г)|₫)'
P_CNY = r'(юан(ями|ей|ем|ям|ях|е|и|ь|ю|я)|Ұ|¥)'

# Теги
P_TAG = r'(#([^\s]+))'
