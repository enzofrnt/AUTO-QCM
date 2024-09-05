from django import template
from colormap import rgb2hex, rgb2hls, hls2rgb

register = template.Library()

@register.filter
def darken_color(hex_color, amount=0.1):
    """
    Assombrit une couleur hexadécimale en ajustant sa luminosité.
    """
    try:
        # Convertir hexadécimal en RGB
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        
        # Convertir RGB en HLS
        h, l, s = rgb2hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
        
        # Réduire la luminosité
        l = max(min(l * (1 - float(amount)), 1.0), 0.0)
        
        # Convertir HLS en RGB
        r, g, b = hls2rgb(h, l, s)
        
        # Convertir RGB en Hex
        darkened_hex = rgb2hex(int(r * 255), int(g * 255), int(b * 255))
        
        return darkened_hex

    except (ValueError, TypeError) as e:
        # En cas d'erreur, retourner la couleur d'origine
        return hex_color