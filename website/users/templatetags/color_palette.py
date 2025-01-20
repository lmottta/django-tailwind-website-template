from django import template
from django.utils.safestring import mark_safe

register = template.Library()

PALETTE_COLORS = {
    'default': {
        'primary': 'from-blue-600 to-blue-800',
        'secondary': 'from-indigo-600 to-indigo-800',
        'accent': 'from-purple-600 to-purple-800',
        'button': 'bg-blue-600 hover:bg-blue-700',
        'button_outline': 'border-blue-600 text-blue-600 hover:bg-blue-600',
        'text': 'text-blue-600',
        'border': 'border-blue-600',
    },
    'nature': {
        'primary': 'from-green-500 to-green-700',
        'secondary': 'from-emerald-500 to-emerald-700',
        'accent': 'from-yellow-500 to-yellow-600',
        'button': 'bg-green-600 hover:bg-green-700',
        'button_outline': 'border-green-600 text-green-600 hover:bg-green-600',
        'text': 'text-green-600',
        'border': 'border-green-600',
    },
    'sunset': {
        'primary': 'from-red-500 to-red-700',
        'secondary': 'from-orange-500 to-orange-700',
        'accent': 'from-yellow-500 to-yellow-600',
        'button': 'bg-red-600 hover:bg-red-700',
        'button_outline': 'border-red-600 text-red-600 hover:bg-red-600',
        'text': 'text-red-600',
        'border': 'border-red-600',
    },
    'ocean': {
        'primary': 'from-blue-400 to-blue-600',
        'secondary': 'from-cyan-500 to-cyan-700',
        'accent': 'from-teal-500 to-teal-700',
        'button': 'bg-blue-500 hover:bg-blue-600',
        'button_outline': 'border-blue-500 text-blue-500 hover:bg-blue-500',
        'text': 'text-blue-500',
        'border': 'border-blue-500',
    },
    'berry': {
        'primary': 'from-purple-500 to-purple-700',
        'secondary': 'from-pink-500 to-pink-700',
        'accent': 'from-fuchsia-500 to-fuchsia-700',
        'button': 'bg-purple-600 hover:bg-purple-700',
        'button_outline': 'border-purple-600 text-purple-600 hover:bg-purple-600',
        'text': 'text-purple-600',
        'border': 'border-purple-600',
    },
    'monochrome': {
        'primary': 'from-gray-600 to-gray-800',
        'secondary': 'from-gray-700 to-gray-900',
        'accent': 'from-gray-500 to-gray-700',
        'button': 'bg-gray-700 hover:bg-gray-800',
        'button_outline': 'border-gray-700 text-gray-700 hover:bg-gray-700',
        'text': 'text-gray-700',
        'border': 'border-gray-700',
    }
}

@register.simple_tag
def get_palette_color(user, color_type):
    """Retorna a classe CSS para o tipo de cor especificado na paleta do usuário"""
    palette = getattr(user, 'color_palette', 'default')
    return PALETTE_COLORS.get(palette, PALETTE_COLORS['default']).get(color_type, '')

@register.simple_tag
def get_gradient(user, direction='to-r'):
    """Retorna as classes CSS para criar um gradiente na direção especificada"""
    palette = getattr(user, 'color_palette', 'default')
    colors = PALETTE_COLORS.get(palette, PALETTE_COLORS['default'])
    return f'bg-gradient-{direction} {colors["primary"]}'

@register.simple_tag
def get_button_class(user, outline=False):
    """Retorna as classes CSS para estilizar um botão de acordo com a paleta do usuário"""
    palette = getattr(user, 'color_palette', 'default')
    colors = PALETTE_COLORS.get(palette, PALETTE_COLORS['default'])
    base_classes = 'btn'
    if outline:
        return f'{base_classes} btn-outline {colors["button_outline"]} hover:text-white'
    return f'{base_classes} {colors["button"]} text-white'
<<<<<<< HEAD

@register.simple_tag(takes_context=True)
def user_color_theme(context):
    request = context['request']
    if request.user.is_authenticated:
        return request.user.color_palette
    return 'default'
=======
>>>>>>> 1bc9d9e56d8d9d501d44190eefe542470fb6ea9f
