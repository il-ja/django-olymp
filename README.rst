****************
Wettbewerbsseite
****************

code für die ultimative Webseite zum Sammeln von allem, was in der Welt der naturwissenschaftlichen Olympiaden relevant ist :-)

„Anleitung“ zum „Mitarbeiten“
=============================

Lokale Kopie erstellen
----------------------

 - git und python3 installieren
 - zum Ordner gehen, in den der Projektordner kommen soll und Konsole öffnen
 - ``git clone https://github.com/il-ja/django-olymp``
 - ``cd django-olymp; git submodule init; git submodule update``
 - optional aber sehr empfohlen: virtual environment installieren:
   ``virtualenv --python=python3 venv`` legt Ordner venv an mit python-Installation die unabhängig vom Rest des Systems ist.
   Alternativ: siehe https://docs.python.org/3/library/venv.html. 
   Später jedes mal die venv aktivieren: ``source venv/bin/activate`` (unter Windoofs anders -> google fragen).
 - alles installieren (vorher venv aktiviert!?) - ``pip install -r requirements.txt``
 - Datenbank kopieren; oder erstmal neue leere erstellen: ``./manage.py migrate``
 - los geht's :) z.B. ``./manage.py runserver``

Änderungen machen und publizieren
---------------------------------

 - Änderungen machen :)
 - ``git status`` (evtl. im Wettbewerbe-Ordner) - prüfen, ob nur das geändert ist was du wolltest
 - wenn ja, dann markiert ``git add .`` alles als publikationsreif; nochmal ``git status`` -> schön grün.
 - noch ein Schritt, beim ersten Mal Identität setzen: ``git config --global user.name "John Doe"; git config --global user.email johndoe@example.com`` (siehe evtl. auch https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
 - ``git commit`` - öffnet prompt, eine commit-message einzugeben - Änderungen kurz aber gut beschreiben!
 - jetzt sind die lokal gesichert, aber wie kriegt man die online? (keine Schreibrechte auf meine repository! - und das ist by design):
 - account bei github anlegen (möglichst mit derselben Mailadresse, mit der die commits geschrieben sind), anmelden, https://github.com/il-ja/app-wettbewerbe öffnen und oben rechts „Fork“ drücken.
 - jetzt gibt es eine repository auf die du schreiben kannst! Nadann: ``git push https://github.com/<dein_name>/app-wettbewerbe``
 - im browser gucken: Änderungen sind da! Auf „new pull request“ gehen, durchklicken, warten bis er gemerged ist :)
 - spoiler: es fühlt sich dann sehr viel einfacher an beim nächsten Mal! :)
