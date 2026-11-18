### Étape 10 – Comprendre et tester une erreur simple

#### Objectif du test

L'objectif de ce test est de provoquer volontairement une erreur simple dans NiFi afin de comprendre son comportement lorsqu'un chemin source est incorrect.

#### Erreur provoquée

Dans les propriétés du processeur **GetFile**, j'ai volontairement renseigné un chemin vers un répertoire source inexistant.

NiFi a détecté le problème et a affiché un message d'erreur indiquant que le répertoire source configuré n'existait pas.

Le message d'erreur a été documenté à l'aide d'une capture d'écran, conservée comme preuve du test réalisé.

**Preuve :** `06_message_erreur_dossier_inexistant.png`

#### Correction appliquée

Pour corriger cette erreur, j'ai remplacé le chemin inexistant dans la propriété **Input Directory** du processeur GetFile par un chemin de répertoire valide :

`/data/nifi/input`

Après application de la modification, le processeur a retrouvé un chemin source valide et a pu reprendre son fonctionnement normal.

#### Bilan du test

Ce test a permis de constater qu'une mauvaise configuration du répertoire source empêche GetFile de fonctionner correctement.

Il a également permis de comprendre l'importance de vérifier les chemins configurés dans les processeurs NiFi et de consulter les messages d'erreur pour identifier l'origine d'un problème.

La correction a consisté à rétablir un chemin de répertoire valide, sans modifier les permissions des répertoires HDFS partagés.