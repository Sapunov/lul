from .extractors import (
    NumberEntity, NumberWithThousandEntity, CurrencyEntity,
    TagEntity, HalfAnHourEntity, HourAndAHalfEntity,
    OneHourEntity, HoursEntity, MinutesEntity,
    HoursMinutesEntity)


EXTRACTORS = (
    NumberEntity,               # 45
    NumberWithThousandEntity,   # 3k
    CurrencyEntity,             # 15 рублей, 40к донг
    TagEntity,                  # #hello_world
    HalfAnHourEntity,           # полчаса
    HourAndAHalfEntity,         # полтора часа
    OneHourEntity,              # час
    HoursEntity,                # 3 часа, 2 с половиной часа
    MinutesEntity,              # 15 минут
    HoursMinutesEntity          # 2 часа 3 минуты, 4 часа 40,
                                # 2 часа и 3 минуты, час 20
)


def preprocess_text(text):
    '''Предобработка текста'''

    return text.strip().lower()


def remove_polysemy(text, entity_list):
    '''Выбор наидлиннейшего термина на данной позиции
        в исходном тексте
    '''

    positions = [False for _ in range(len(text))]
    entity_list.sort(key=lambda it: it.size, reverse=True)
    approved_entities = []

    def lock_positions(start, end, positions):
        for i in range(start, end):
            positions[i] = True

    def is_vacant(start, end, positions):
        for i in range(start, end):
            if positions[i]:
                return False
        return True

    for entity in entity_list:
        if is_vacant(entity.start, entity.end, positions):
            approved_entities.append(entity)
            lock_positions(entity.start, entity.end, positions)

    approved_entities.sort(key=lambda it: it.start)

    return approved_entities


def extract_entities(text, extractors=EXTRACTORS):
    '''Извлечение сущностей'''

    text = preprocess_text(text)

    if extractors is None:
        return []

    entities = []
    for extractor in extractors:
        entities.extend(extractor.extract(text))
    entities = remove_polysemy(text, entities)

    return entities
