from django import template

register = template.Library()

@register.inclusion_tag('Kommentare/kommentarliste_kommentar.html')
def kommentare(liste, nutzer):
    """ Der tag fügt in einer Schleife (s. obiges template) je einen
    Eintrag zu den Elementen der hier übergebenen Liste ein. 
    Die Elemente sind paare (kommentar, ob_nutzer_editieren_darf)
    """
    #import ipdb; ipdb.set_trace() 
    alle_kommentare = liste.kommentare.all()
    if not nutzer.is_authenticated:
        liste_paare = [
            (kommentar, False) 
            for kommentar in liste.kommentare.all()
        ]
    else:
        liste_paare = [
            (kommentar, kommentar in nutzer.kommentare.all())
            for kommentar in liste.kommentare.all()
        ]
    return {'kommentare': liste_paare}

@register.simple_tag
def darf_editieren(nutzer, kommentar):
    return kommentar.autor == nutzer
