from django import template
import urllib.parse

register = template.Library()

@register.filter(name='ui_avatar')
def ui_avatar(name, size=40):
    name_encoded = urllib.parse.quote(name)
    return f"https://ui-avatars.com/api/?name={name_encoded}&size={size}&background=random&color=fff"
