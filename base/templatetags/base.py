from json import dumps as json_dumps
import markdown
from django import template
from django.utils.safestring import mark_safe

from statblocks.models import Action, Monster, StatblockBit, AbilityScore
from base.utils import Die
from places.models import Place
from places.serializers import PlaceLiteSerializer, PlaceSerializer

register = template.Library()


@register.simple_tag(takes_context=True)
def breakpoint_with_context(context):
    pass


@register.filter
def get_attr(obj, accessor):
    if hasattr(obj, accessor):
        return getattr(obj, accessor)
    else:
        return ''


@register.filter
def print_type_and_return(value):
    print(type(value))
    return value


@register.filter
def print_and_return(value):
    print(value)
    return value


@register.simple_tag
def val_in_iterable_in_dict_under_key(val, _dict, key):
    if _dict.get(key):
        _iterable = _dict[key]
        for item in _iterable:
            if str(item) == str(val):
                return True
    return False


@register.filter
def multiply(value, arg):
    return value * arg


@register.simple_tag
def get_attack_to_hit_for_monster(attack: Action, monster: Monster):

    mod_to_get = '{}_mod'.format(attack.attack_uses)
    if hasattr(monster, mod_to_get) and monster.proficiency is not None:
        return monster.proficiency + int(getattr(monster, mod_to_get))
    else:
        return 0


@register.filter
def range_or_reach_text(attack: Action):
    if not attack.attack_type:
        return ''
    if attack.attack_type in [Action.MELEE_WEAPON_ATTACK, Action.MELEE_SPELL_ATTACK]:
        return 'reach {}'.format(attack.get_reach_range_display())
    elif attack.range_secondary:  # ranged weapon attack or a ranged spell attack with a second range increment
        return 'range {}/{} ft.'.format(attack.reach_range, attack.range_secondary)
    else:  # ranged spell attack or a ranged weapon attack without a second range increment
        return 'range {}'.format(attack.get_reach_range_display())


@register.simple_tag
def avg_with_die_in_parens(num_die, die_type, constant_to_add=None):
    avg = Die.expected_value(num=num_die, size=die_type)
    if constant_to_add is None or constant_to_add == 0:
        return '{} ({}d{})'.format(avg, num_die, die_type)
    elif constant_to_add > 0:
        return '{} ({}d{} + {})'.format(
            avg + constant_to_add,
            num_die,
            die_type,
            constant_to_add
        )
    else:
        return '{} ({}d{} - {})'.format(
            avg + constant_to_add,
            num_die,
            die_type,
            -1*constant_to_add
        )


@register.filter
def get_mod(monster: Monster, mod):
    mod_to_get = '{}_mod'.format(mod)
    if hasattr(monster, mod_to_get):
        return getattr(monster, mod_to_get)
    else:
        return -5


@register.filter
def replace_generic_monster(description: str, monster: Monster=None):
    if description is None:
        return ''
    GENERIC_MONSTER_TAG = '$monster$'
    if monster is None:
        replace_with = 'monster'
    else:
        replace_with = monster.statblock_generic_name
    return description.replace(GENERIC_MONSTER_TAG, replace_with)


@register.filter
def fill_generic_statblock_descr(statbit: StatblockBit, monster: Monster=None):
    GENERIC_MONSTER_TAG = '$monster$'
    GENERIC_DC_TAG = '$dc$'
    GENERIC_SAVETYPE_TAG = '$savetype$'

    if statbit.description is None:
        return ''
    else:
        to_return = statbit.description
        if monster is not None:
            to_return = to_return.replace(
                GENERIC_MONSTER_TAG, monster.statblock_generic_name
            )
        if statbit.save_dc is not None:
            to_return = to_return.replace(
                GENERIC_DC_TAG, str(statbit.save_dc)
            )
        if statbit.save_type is not None:
            to_return = to_return.replace(
                GENERIC_SAVETYPE_TAG, str(AbilityScore.get_full_name(statbit.save_type)).title()
            )
        return to_return


@register.filter
def markdownify(text):
    return markdown.markdown(text, safe_mode='escape', extensions=[
        'markdown.extensions.nl2br',
        'markdown.extensions.tables',
        'markdown.extensions.sane_lists',
    ])


@register.filter
def user_props_json(user):
    try:
        props = {
            'is_authenticated': user.is_authenticated
        }
    except AttributeError:
        props = {}
    return mark_safe(json_dumps(props))


@register.filter
def place_json(place):
    if not place:
        return ''
    elif isinstance(place, Place):
        serializer = PlaceSerializer(place)
    else:
        serializer = PlaceLiteSerializer(place, many=True)
    return mark_safe(json_dumps(serializer.data))


@register.simple_tag(takes_context=True)
def template_context_to_json(context):
    to_return = {}
    api_url = context.get('api_url', None)
    if api_url:
        to_return['api_url'] = api_url
    user = context.get('user', None)
    profile = None
    if user:
        to_return['user'] = {
            'is_authenticated': user.is_authenticated
        }
        if user.is_authenticated:
            profile = user.profile
    # todo - alternative way of getting profile 
    if profile:
        campaign = profile.cur_campaign
        if campaign:
            to_return['campaign'] = {
                'place_inclusion_distance': campaign.place_inclusion_distance
            }

    return mark_safe(json_dumps(to_return))
