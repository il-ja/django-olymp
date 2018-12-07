from django import template
from django.contrib.auth import get_user_model

register = template.Library()

@register.inclusion_tag('Grundgeruest/kopfzeile_knopf.html')
def kopfleiste_knoepfe(user):
    """ Der tag erwartet von der Funktion ein dict, in dem die Liste der
    url-text-Paare für die Knöpfe der Kopfleiste steht """

    return {'knoepfe': get_user_model().knoepfe_kopf(user)}

@register.inclusion_tag('Grundgeruest/menueleiste_knopf.html')
def menueleiste_knoepfe(user):
    """ gibt ein dict zurück, in dem die Liste der url-text-Paare für die
    Knöpfe der Menüleiste steht """

    return {'knoepfe': get_user_model().knoepfe_menü(user)}

@register.inclusion_tag('Grundgeruest/listeneintrag.html')
def listeneintrag(objekt, request, nur_link=False):
    """ Templatetag wird für eine Verknüpfung zu Objekten, zu denen es
    eine Detailseite gibt, verwendet; z.B. für einen Punkt innerhalb
    einer Liste. Falls der request zu einem admininterface-berechtigten
    gehört, folgt hinter dem normalen Link ein Link zur entsprechenden
    Seite unter /admin/[...change-view]
    """

    return {
        'objekt': objekt,
        'ob_zeigen': request.user.is_staff,
        'nur_link': nur_link,
        'admin_link': '/admin/{app}/{model}/{pk}/change'.format(
            app=objekt.__class__.__module__.split('.')[0].capitalize(),
            model=objekt.__class__.__name__.lower(),
            pk=objekt.pk,
        ),
    }
