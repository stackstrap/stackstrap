import random
import string

from django import template

register = template.Library()

@register.simple_tag
def random_secret(length=96):
    pool = string.ascii_letters + string.digits
    return "".join([
        random.choice(pool)
        for x in xrange(length)
        ])
