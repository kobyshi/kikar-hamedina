# -*- coding: utf-8 -*-
import re
from urllib2 import unquote
from django import template
from django.utils import timezone
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.dateformat import format

register = template.Library()


@register.filter(name='normalize')
def normalize(value):
    if value:
        return value
    return ''


@register.filter(name='link')
def link(status):
    """Returns the post link for a status"""
    split_id = status.status_id.split('_')
    return 'https://www.facebook.com/%s/posts/%s' % (split_id[0], split_id[1])


@register.filter(name='percent')
def percent(value):
    if value is None:
        return None
    return floatformat(value * 100.0, 2) + '%'


@register.filter(name='urldecode')
def unquote_new(value):
    return unquote(value).decode()


@register.filter(name='render_icons')
def render_icons(value):
    if '#like' in value:
        return value.replace('#like', '<i class="fa fa-thumbs-up"></i>')
    else:
        return value


@register.filter(name='append_separators')
def append_separators(value):
    def add_newline(matchobj):
        return '\n' + matchobj.group(0) + '\n'

    return re.sub('\n[*=]+\n', add_newline, value)


@register.filter(name='path_to_params')
def path_to_params(path):
    return u'?{}'.format(path.split('?')[-1])


@register.filter(name='language_clean_uri')
def language_clean_uri(uri):
    return uri.split('/en')[-1].split('/ar')[-1].split('/he')[-1]

@register.filter(name='naturaltime_ext')
def naturaltime_ext(value, locale):
    formatted_value = ''

    if locale != 'he':
        formatted_value = 'Published: '

    time_differ = timezone.now() - value
    if time_differ.days < 7:
        formatted_value += naturaltime(value)
    else:
        if locale != 'he':
            formatted_value += format(value, 'F jS, Y, g a')
        else:
            formatted_value += format(value, 'j בF Y, H:i')

    return formatted_value
