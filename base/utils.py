from datetime import datetime
from pytz import utc
from django.db.models import base, Model

from .models import TableMetaData


def update_last_updated(model: Model):
    table_name = model._meta.db_table
    metadata = None
    try:
        metadata = TableMetaData.objects.get(which_table=table_name)
    except base.ObjectDoesNotExist as e:
        metadata = TableMetaData(which_table=table_name)

    if metadata is None:
        return None

    now = datetime.utcnow()
    now = utc.localize(now)
    metadata.last_updated = now
    metadata.save()
    return now


class Size:
    TINY, SMALL, MEDIUM, LARGE, HUGE, GARGANTUAN, COLOSSAL = 1, 2, 3, 4, 5, 6, 7
    MODEL_CHOICES = [(TINY, 'Tiny'), (SMALL, 'Small'), (MEDIUM, 'Medium'), (LARGE, 'Large'), (HUGE, 'Huge'),
                     (GARGANTUAN, 'Gargantuan'), (COLOSSAL, 'Colossal'), ]


class Alignment:
    UNALIGNED = 0
    LAWFUL_GOOD, NEUTRAL_GOOD, CHAOTIC_GOOD = 1, 2, 3
    LAWFUL_NEUTRAL, NEUTRAL, CHAOTIC_NEUTRAL = 4, 5, 6
    LAWFUL_EVIL, NEUTRAL_EVIL, CHAOTIC_EVIL = 7, 8, 9

    MODEL_CHOICES = [
        (LAWFUL_GOOD, 'lawful good'), (NEUTRAL_GOOD, 'neutral good'), (CHAOTIC_GOOD, 'chaotic good'),
        (LAWFUL_NEUTRAL, 'lawful neutral'), (NEUTRAL, 'neutral'), (CHAOTIC_NEUTRAL, 'chaotic neutral'),
        (LAWFUL_EVIL, 'lawful evil'), (NEUTRAL_EVIL, 'neutral evil'), (CHAOTIC_EVIL, 'chaotic evil'),
        (UNALIGNED, 'unaligned')
    ]


class Die:
    d2 = 2
    d3 = 3
    d4 = 4
    d6 = 6
    d8 = 8
    d10 = 10
    d12 = 12
    d20 = 20
    d100 = 100
    MODEL_CHOICES = [
        (d4, 'd4'),
        (d6, 'd6'),
        (d8, 'd8'),
        (d10, 'd10'),
        (d12, 'd12'),
        (d20, 'd20'),
        (d100, 'd100'),
    ]


class DamageType:
    BLUDGEONING, PIERCING, SLASHING, PHYSICAL = 1, 2, 3, 4
    PHYSICAL_NON_MAGICAL, PHYSICAL_NON_SILVERED = 5, 6
    FIRE, COLD, ACID, LIGHTNING, THUNDER = 7, 8, 9, 10, 11
    POISON, PSYCHIC, FORCE = 12, 13, 14
    RADIANT, NECROTIC = 15, 16
    MODEL_CHOICES = [
        (BLUDGEONING, 'bludgeoning'),
        (PIERCING, 'piercing'),
        (SLASHING, 'slashing'),
        (PHYSICAL, 'bludgeoning, piercing, and slashing'),
        (PHYSICAL_NON_MAGICAL, 'bludgeoning, piercing, and slashing from nonmagical attacks'),
        (PHYSICAL_NON_SILVERED,
         'bludgeoning, piercing, and slashing from nonmagical attacks not made with silvered weapons'),
        (FIRE, 'fire'),
        (COLD, 'cold'),
        (ACID, 'acid'),
        (LIGHTNING, 'lightning'),
        (THUNDER, 'thunder'),
        (POISON, 'poison'),
        (PSYCHIC, 'psychic'),
        (FORCE, 'force'),
        (RADIANT, 'radiant'),
        (NECROTIC, 'necrotic'),
    ]


class Condition:
    BLINDED, CHARMED, DEAFENED, FRIGHTENED, GRAPPLED, INCAPACITATED = 1, 2, 3, 4, 5, 6
    INVISIBLE, PARALYZED, PETRIFIED, POISONED, PRONE, RESTRAINED = 7, 8, 9, 10, 11, 12
    STUNNED, UNCONSCIOUS = 13, 14
    MODEL_CHOICES = [
        (BLINDED, 'blinded'),
        (CHARMED, 'charmed'),
        (DEAFENED, 'deafened'),
        (FRIGHTENED, 'frightened'),
        (GRAPPLED, 'grappled'),
        (INCAPACITATED, 'incapacitated'),
        (INVISIBLE, 'invisible'),
        (PARALYZED, 'paralyzed'),
        (PETRIFIED, 'petrified'),
        (POISONED, 'poisoned'),
        (PRONE, 'prone'),
        (RESTRAINED, 'restrained'),
        (STUNNED, 'stunned'),
        (UNCONSCIOUS, 'unconscious'),
    ]


class Language:
    COMMON, DWARVISH, ELVISH = 1, 2, 3
    GIANT, GOBLIN, ORC = 4, 5, 6
    GNOMISH, HALFLING = 7, 8
    ABYSSAL, CELESTIAL, INFERNAL = 9, 10, 11
    DRACONIC, SYLVAN = 12, 13
    PRIMORDIAL, AURAN, AQUAN, IGNAN, TERRAN = 14, 15, 16, 17, 18
    UNDERCOMMON, DEEP_SPEECH = 19, 20
    DRUIDIC, THIEVES_CANT = 21, 22
    TELEPATHY, TELEPATHY_30, TELEPATHY_60, TELEPATHY_120 = 23, 24, 25, 26

    MODEL_CHOICES = [
        (COMMON, 'Common'),
        (DWARVISH, 'Dwarvish'), (ELVISH, 'Elvish'),
        (GIANT, 'Giant'), (GOBLIN, 'Goblin'), (ORC, 'Orc'),
        (GNOMISH, 'Gnomish'), (HALFLING, 'Halfling'),
        (ABYSSAL, 'Abyssal'), (CELESTIAL, 'Celestial'), (INFERNAL, 'Infernal'),
        (DRACONIC, 'Draconic'), (SYLVAN, 'Sylvan'),
        (PRIMORDIAL, 'Primordial'), (AURAN, 'Auran'), (AQUAN, 'Aquan'), (IGNAN, 'Ignan'), (TERRAN, 'Terran'),
        (UNDERCOMMON, 'Undercommon'), (DEEP_SPEECH, 'Deep Speech'),
        (DRUIDIC, 'Druidic'), (THIEVES_CANT, "Thieve's Cant"),
        (TELEPATHY, 'Telepathy'), (TELEPATHY_30, 'Telepathy 30 ft.'),
        (TELEPATHY_60, 'Telepathy 60 ft.'), (TELEPATHY_120, 'Telepathy 120 ft.')
    ]

    class Script:
        COMMON = 1
        DWARVISH = 2
        ELVISH = 3
        INFERNAL = 4
        CELESTIAL = 5
        DRACONIC = 6

        _script_name_dict = {
            COMMON: 'common',
            DWARVISH: 'dwarvish',
            ELVISH: 'elvish',
            INFERNAL: 'infernal',
            CELESTIAL: 'celestial',
            DRACONIC: 'draconic',
        }

        @classmethod
        def name(cls, script):
            try:
                return cls._script_name_dict[script]
            except KeyError:
                return None

    _script_dict = {
        COMMON: Script.COMMON,
        DWARVISH: Script.DWARVISH,
        ELVISH: Script.ELVISH,
        GIANT: Script.DWARVISH,
        GNOMISH: Script.DWARVISH,
        GOBLIN: Script.DWARVISH,
        HALFLING: Script.COMMON,
        ORC: Script.DWARVISH,
        ABYSSAL: Script.INFERNAL,
        CELESTIAL: Script.CELESTIAL,
        DRACONIC: Script.DRACONIC,
        DRUIDIC: Script.ELVISH,
        INFERNAL: Script.INFERNAL,
        PRIMORDIAL: Script.DWARVISH,
        SYLVAN: Script.ELVISH,
        UNDERCOMMON: Script.ELVISH,
    }

    @classmethod
    def script_name(cls, language):
        try:
            return cls.Script.name(cls._script_dict[language])
        except KeyError:
            return None
