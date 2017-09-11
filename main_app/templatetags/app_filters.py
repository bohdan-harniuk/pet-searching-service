from django import template

register = template.Library()

@register.filter(name="get_value_by_key")
def get_value_by_key(dictionary, key):
    return dictionary.get(key)

@register.filter(name="get_value_by_key_mod")
def get_value_by_key(dictionary, key):
    original_string = dictionary.get(key)
    pos = original_string.find(':')
    return original_string[(pos+1):]

@register.filter(name="get_pet_type")
def get_pet_type(pet_type):
    if pet_type == 'Собака':
        return pet_type
    elif pet_type == 'Кішка':
        return pet_type
    elif pet_type == 'Птах':
        return 'Пташка'
    elif pet_type == 'Малий ссавець':
        return 'Тварина'
    elif pet_type == 'Рептилія':
        return pet_type
    else:
        return 'Тварина'