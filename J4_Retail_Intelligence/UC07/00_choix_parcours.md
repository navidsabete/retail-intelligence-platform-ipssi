## Choix du parcours de réalisation – Parcours B : Local / Open Source

Dans le cadre du UC-07, le choix s'est porté sur le **Parcours B – Local / Open Source**, conformément aux possibilités proposées dans les consignes du TP.

Cette décision repose sur plusieurs considérations :

- La volonté de poursuivre le projet dans l'environnement Linux déjà utilisé pour les précédentes UCs.
- La continuité avec l'architecture Data Lake / Data Warehouse / Lakehouse mise en place et étudiée précédemment.
- La volonté de limiter les dépendances à des services cloud externes.
- La maîtrise des coûts et la réduction du risque lié à l'utilisation d'un abonnement Azure potentiellement facturé.

Ce parcours permet de réaliser la transposition fonctionnelle de l'architecture vers les services Azure tout en conservant une mise en œuvre locale fondée sur les technologies Open Source.

L'environnement existant, notamment Python, PySpark, Apache Spark et Parquet, constitue le socle technique de cette démarche.

Le choix du parcours local ne signifie toutefois pas que l'environnement cloud est écarté définitivement.

**Une migration ou une extension future vers Microsoft Azure reste une perspective d'évolution envisageable pour Retail Intelligence.** Elle pourrait notamment permettre de bénéficier d'un stockage centralisé avec Azure Data Lake Storage Gen2, de services d'intégration avec Azure Data Factory et de capacités analytiques avec Azure Synapse Analytics.

Le UC-07 permettra ainsi d'étudier cette évolution potentielle, d'identifier les correspondances entre les composants locaux et les services Azure, et d'en évaluer les avantages et les limites, sans procéder à un déploiement cloud effectif.

Les composants Azure seront donc étudiés et documentés, tandis que les composants locaux seront présentés en distinguant ceux effectivement utilisés de ceux qui restent à l'état de proposition.