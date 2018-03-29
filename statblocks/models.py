from django.db import models
from django.forms import ModelForm

from multiselectfield import MultiSelectField

from base.models import BaseModel


class Size:
    TINY, SMALL, MEDIUM, LARGE, HUGE, GARGANTUAN, COLOSSAL = 1, 2, 3, 4, 5, 6, 7
    MODEL_CHOICES = [(TINY, 'Tiny'), (SMALL, 'Small'), (MEDIUM, 'Medium'), (LARGE, 'Large'), (HUGE, 'Huge'),
                     (GARGANTUAN, 'Gargantuan'), (COLOSSAL, 'Colossal'), ]


class Alignment:
    LAWFUL_GOOD, NEUTRAL_GOOD, CHAOTIC_GOOD, LAWFUL_NEUTRAL, NEUTRAL, CHAOTIC_NEUTRAL, LAWFUL_EVIL, NEUTRAL_EVIL, CHAOTIC_EVIL = 1, 2, 3, 4, 5, 6, 7, 8, 9
    MODEL_CHOICES = [
        (LAWFUL_GOOD, 'Lawful good'), (NEUTRAL_GOOD, 'Neutral good'), (CHAOTIC_GOOD, 'Chaotic good'),
        (LAWFUL_NEUTRAL, 'Lawful neutral'), (NEUTRAL, 'Neutral'), (CHAOTIC_NEUTRAL, 'Chaotic neutral'),
        (LAWFUL_EVIL, 'Lawful evil'), (NEUTRAL_EVIL, 'Neutral evil'), (CHAOTIC_EVIL, 'Chaotic evil')
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

    MODEL_CHOICES = [
        (COMMON, 'Common'),
        (DWARVISH, 'Dwarvish'), (ELVISH, 'Elvish'),
        (GIANT, 'Giant'), (GOBLIN, 'Goblin'), (ORC, 'Orc'),
        (GNOMISH, 'Gnomish'), (HALFLING, 'Halfling'),
        (ABYSSAL, 'Abyssal'), (CELESTIAL, 'Celestial'), (INFERNAL, 'Infernal'),
        (DRACONIC, 'Draconic'), (SYLVAN, 'Sylvan'),
        (PRIMORDIAL, 'Primordial'), (AURAN, 'Auran'), (AQUAN, 'Aquan'), (IGNAN, 'Ignan'), (TERRAN, 'Terran'),
        (UNDERCOMMON, 'Undercommon'), (DEEP_SPEECH, 'Deep Speech'),
        (DRUIDIC, 'Druidic'), (THIEVES_CANT, "Thieve's Cant")
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


class Monster(BaseModel):
    size = models.IntegerField(choices=Size.MODEL_CHOICES, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    alignment = models.IntegerField(choices=Alignment.MODEL_CHOICES, null=True, blank=True)
    armor_class = models.IntegerField(null=True, blank=True)
    armor_kind = models.CharField(max_length=255, null=True, blank=True)
    hit_points = models.IntegerField(null=True, blank=True)
    num_hit_die = models.IntegerField(null=True, blank=True)
    hit_die_size = models.IntegerField(choices=Die.MODEL_CHOICES, null=True, blank=True)
    speed = models.CharField(max_length=100, null=True, blank=True)
    str = models.IntegerField(null=True, blank=True)
    dex = models.IntegerField(null=True, blank=True)
    con = models.IntegerField(null=True, blank=True)
    int = models.IntegerField(null=True, blank=True)
    wis = models.IntegerField(null=True, blank=True)
    cha = models.IntegerField(null=True, blank=True)

    @property
    def str_mod(self):
        return (self.str - 10) // 2

    @property
    def dex_mod(self):
        return (self.dex - 10) // 2

    @property
    def con_mod(self):
        return (self.con - 10) // 2

    @property
    def int_mod(self):
        return (self.int - 10) // 2

    @property
    def wis_mod(self):
        return (self.wis - 10) // 2

    @property
    def cha_mod(self):
        return (self.cha - 10) // 2

    saving_throws = models.CharField(max_length=50, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    damage_vulnerabilities = MultiSelectField(choices=DamageType.MODEL_CHOICES, null=True, blank=True)
    damage_resistances = MultiSelectField(choices=DamageType.MODEL_CHOICES, null=True, blank=True)
    damage_immunities = MultiSelectField(choices=DamageType.MODEL_CHOICES, null=True, blank=True)
    condition_immunities = MultiSelectField(choices=Condition.MODEL_CHOICES, null=True, blank=True)
    senses = models.CharField(max_length=255, null=True, blank=True)
    languages = models.IntegerField(choices=Language.MODEL_CHOICES, null=True, blank=True)
    challenge = models.CharField(
        max_length=3,
        choices=[
            '0', '1/8', '1/4', '1/2'
        ].extend(['{}'.format(num) for num in range(1, 31)]),
        null=True, blank=True
    )

    # special_properties = models.ManyToManyField()
    # actions = models.ManyToManyField


class MonsterForm(ModelForm):
    class Meta:
        model = Monster
        fields = '__all__'
