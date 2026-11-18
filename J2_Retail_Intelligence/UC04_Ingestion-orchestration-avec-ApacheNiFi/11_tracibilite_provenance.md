### Étape 11 – Traçabilité et provenance du FlowFile

La consultation de l'historique de provenance dans NiFi a permis d'identifier deux événements associés au même FlowFile.

Le FlowFile possède l'identifiant UUID suivant :

`82e1a02d-5f46-49d0-8b97-e396380536bd`

Les événements observés sont les suivants :

- **RECEIVE – GetFile**, le 18 novembre 2026 à 11:26:42.501 CET : prise en charge du fichier depuis le répertoire local d'entrée.
- **SEND – PutHDFS**, le 18 novembre 2026 à 11:26:43.123 CET : envoi du FlowFile vers la destination HDFS.

La taille du FlowFile est de 12,66 MB pour les deux événements. Le même identifiant UUID permet d'établir le lien entre la lecture locale et l'envoi vers HDFS.

Ces informations permettent de reconstituer le parcours du fichier, d'identifier les composants traversés, de connaître les horaires de traitement et de suivre un FlowFile de manière individuelle.