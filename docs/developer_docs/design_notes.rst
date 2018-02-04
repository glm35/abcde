Notes de conception pour abcde
==============================

Retour musical (Musical feedback)
---------------------------------

Le but de la fonctionnalité de retour musical est d'entendre les notes au
moment de la saisie. Cela permet d'entendre immédiatement les erreurs de
saisie et de les corriger au plus tôt.

Principes de base
~~~~~~~~~~~~~~~~~

* Quand on est dans un contexte de commentaire (derrière `%`) ou dans un champ
  informatif, il n'y a pas de feedback musical.

* Sinon, quand on appuie sur une touche correspondant à une note de musique, la
  note est jouée **immédiatement** (comme sur un piano): la note est jouée sur
  l'évènement *key press*, et pas sur l'évènement *key release*.

* La tonalité du morceau et les altérations accidentelles sont prises en
  compte. C'est faisable parce que dans le format ABC, ces informations sont
  saisies avant les notes. Exemple: `cde ^fga`: le symbole `^` qui signifie
  *dièse* est placé avant la note.

Marqueurs d'octave
~~~~~~~~~~~~~~~~~~

Le format ABC version 1.6 permet de saisir les notes sur 4 octaves:

* notes en majuscules, à partir de `C`: à partir du c4 de la norme MIDI (numéro
  de note 60)

* notes en minuscules, à partir de `c`: une octave plus haut, à partir de la
  note MIDI 72

* notes en minuscules suivie de *une* apostrophe, à partir de `c'`: encore une
  octave plus haut, à partir de la note MIDI 84

* notes en majuscules suvies de *une* virgule, à partir de `C,`: une octave en
  dessous de `C`, à partir de la note MIDI 58.

En résumé: le format ABC 1.6 permet de saisir un sous-ensemble des notes
disponibles sur un clavier MIDI, allant de la note 48 (C3) à la note à la note
95 (B6). Pour la correspondance entre les notes et leur numéro MIDI, voir par
exemple `Note names, MIDI numbers and frequencies`_.

Comment faire entendre un retour musical sur les notes suivies d'une virgule ou
d'une apostrophe? Dans ce cas, la virgule ou l'apostrophe est saisie après la
note, et le logiciel ne peut pas deviner ce qui va se passer.

Liste d'options possibles:

.. _jouer-deux-fois-la-note:

jouer deux fois la note

   La note est jouée au moment où elle est saisie, avec une octave
   correspondant à sa casse. Puis elle est jouée une seconde fois après la
   saisie de la virgule (note en majuscule) ou de l'apostrophe (note en
   minuscule).

attendre un petit peu avant de jouer la note

   On laisse à l'utilisateur le temps de saisir un marqueur d'octave avant de
   jouer la note (eg 500ms).
   
   Inconvénient: on perd l'effet piano (note jouée immédiatement lors de
   l'appui).

maintenir une autre touche appuyée

   L'utilisateur maintient une touche appuyée durant la saisie de la note et de
   la modification d'octave. La note est jouée au relâchement de cette touche.

   Là aussi, on perd l'effet piano.
   
   D'autre part, le choix de la touche de modification n'est pas évident:
   `Shift` est déjà utilisé pour choisir entre les notes majuscules et
   minuscules; `Ctrl` et `Alt` sont utilisées pour les raccourcis clavier de
   l'application ou du gestionnaire de fenêtre. Et si on maintient une note
   appuyée (eg `c`), l'application va recevoir des appuis multiples.

configurer une translation d'octave

   L'utilisateur configure une translation d'octave (une octave au dessus, ou
   une octave au dessous).

   Avec la configuration *une octave au dessus*, les `C` sont saisis et joués
   `c` et les `c` sont saisis et joués `c'`.

   Avec la configuration *une octave au dessous*, les `C` sont saisis et joués
   `C,` et les `c` sont saisis et joués `C`.

   Dans ce cas, le logiciel fait de la saisie automatique: des caractères non
   entrés par l'utilisateur apparaissent dans la zone d'édition.

La solution retenue pour abcde est l'approche :ref:`jouer deux fois la note
<jouer-deux-fois-la-note>`. A terme, une des autres approches pourrait être
mise en oeuvre pour gérer les passages musicaux relativement longs nécessitant
l'usage des marqueurs d'octave. Cette autre approche pourrait être
complémentaire.

.. _Note names, MIDI numbers and frequencies: http://newt.phys.unsw.edu.au/jw/notes.html


Encodage des fichiers ABC
-------------------------

abcde travaille avec le format UTF-8:

* abcde enregistre toujours les fichiers avec l'encodage UTF-8

* abde ne peut ouvrir que des fichiers encodés en UTF-8. Si ce n'est pas le cas, il faut les convertir
  en UTF-8 avant de les ouvrir avec abcde.

.. note::

   Sous Linux,  le programme ``file`` implémente des heuristiques pour essayer de découvrir l'encodage
   d'un fichier texte et le programme ``iconv`` permet de transcoder les caractères d'un fichier.

   Exemple pour réaliser une conversion ISO-8859-1 vers UTF-8::

     $ file gwen_random_tunes.abc
     gwen_random_tunes.abc: ISO-8859 text

     $ iconv -f ISO-8859-1 -t UTF-8 gwen_random_tunes.abc > gwen_random_tunes.abc.utf8

     $ file gwen_random_tunes.abc.utf8
     gwen_random_tunes.abc.utf8: UTF-8 Unicode text


Composition des objets tkinter
------------------------------

Les objets d'IHM d'abcde ne sont pas hérités de tkinter: on va plutôt les inclure dans nos classes
(composition plutôt que héritage). La raison est d'éviter une surcharge accidentelle (shadowing?)
des attributs et méthodes des objets tkinter.

.. _Fichiers récents et favoris:

Fichiers favoris et fichiers récemment édités
---------------------------------------------

Fichiers récents et favoris v1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans cette première version, on traite uniquement le cas des fichiers favoris:

  * les fichiers favoris sont stockés dans ~/.config/abcde/favorite_files.txt

    * favorite_files.txt est encodé en UTF-8. Si ce n'est pas le cas, un warning est affiché
      dans les logs et le fichier n'est pas traité

    * on peut définir autant de fichiers favoris qu'on le souhaite

    * les chemins sont absolus ou relatifs; un chemin relatif sera par rapport au répertoire de
      démarrage d'abcde; un chemin relatif sera présenté comme un chemin absolu dans le menu

    * un chemin peut commencer par ~/: il est alors relatif à la racine du répertoire personnel
      de l'utilisateur courant.

    * une ligne commençant par # est considérée comme un commentaire et non traitée

    * une ligne vide est non traitée

    * on valide le format de chaque ligne: vérification syntaxique que c'est bien un chemin,
      avec une approche multiplateforme. Si ce n'est pas le cas, un warning est affiché
      dans les logs et le fichier n'est pas affiché dans les menus

  * on édite la liste manuellement en dehors d'abcde

  * la liste est lue uniquement au démarrage d'abcde, et les fichiers favoris apparaissent dans le
    menu fichier.

Fichiers récents et favoris v2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  * conserver les 6 fichiers les plus récemment ouverts dans ~/.config/abcde/recent_files.txt

    * on ajoute un fichier récent dans la liste dès qu'on ouvre un fichier ou qu'on enregistre
      un fichier sous un nouveau nom; on enregistre recent_files.txt immédiatement.

  * essayer de se conformer au standard "XDG Base Directory Specification"
    https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    pour l'emplacement des fichiers

  * afficher dans une même liste dans le menu fichier les fichiers favoris et les fichiers récents

    * les fichiers favoris sont identifiés par une icone "étoile"

    * on affiche d'abord les fichiers récents puis les fichiers favoris

    * un fichier à la fois récent et favori est affiché dans la première partie de la liste (fichiers récents)
      avec son icone de fichier favori

Fichiers récents et favoris v3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  * pouvoir ajouter/retirer des fichiers favoris depuis l'application

  * approches possibles:

    * approche 1: une icone étoile pleine ou vide devant chaque fichier favori ou récent du menu; en cliquant sur
      l'icone, on change l'état du fichier: favori ou non

    * approche 2: une commande menu pour "Ajouter le fichier courant aux favoris" ou "Retirer le fichier courant
      des favoris", selon que le fichier courant est déjà favori ou pas.