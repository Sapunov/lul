import random

import misc


# TODO: Переписать более просто, а то какая-то хуйня сложная


class IPhrase:

    def get_phrase(self):

        raise NotImplementedError()


class Phrase(IPhrase):

    def __init__(self, name, phrase_text):

        self.name = name
        self.text = phrase_text

    def get_phrase(self):

        return self.text


class RandomPhrase(IPhrase):

    def __init__(self, name, phrases_list):

        assert isinstance(phrases_list, list), '`phrases_list` must be of type list'

        self.name = name
        self.items = phrases_list

    def get_phrase(self):

        variants = random.sample(self.items, 1)
        return variants[0]


PHRASES = [
    RandomPhrase('start', [
        'Привет! Напишите первое событие, которое вы хотите залогировать',
        'Алоха! Скорее пишите свое первое сообщение, которое я смогу обработать'
        ]),
    Phrase('help', 'Помощи ждать не от кого, друг мой'),
    Phrase('unknown', 'Какое-то странное у вас сообщение. Не знаю что и сказать 😞'),
    RandomPhrase('wait', [
        'Секундочку...',
        'Один момент...',
        'Работаю, ожидайте...']),
    RandomPhrase('edit', [
        'Записал новую версию',
        'Хорошо, сохранил исправления'
        ]),
    RandomPhrase('saved', [
        'Все, сохранил',
        'Занес в базу'
    ])
]


class Phrases(metaclass=misc.Singleton):

    def __init__(self):

        self._phrases = {}

        for phrase in PHRASES:
            if not phrase.name in self._phrases:
                self._phrases[phrase.name] = phrase
            else:
                raise ValueError('Phrase has duplicated name')

    def __getattr__(self, attr_name):

        if attr_name in self._phrases:
            return self._phrases[attr_name].get_phrase()
        else:
            raise ValueError()
