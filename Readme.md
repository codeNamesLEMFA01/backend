# Nom du Projet

Ce projet utilise Docker Compose pour mettre en place un environnement de développement comprenant une application web, une base de données MongoDB et Mongo Express pour la gestion de la base de données.

## Prérequis

- Docker
- Docker Compose

## Services

### Application Web

- Nom du conteneur : `code-name-web`
- Port : 8000
- Dépend du service MongoDB
- Monte le répertoire courant en tant que volume en lecture seule

### MongoDB

- Nom du conteneur : `code-name-db`
- Image : mongo:7.0.5
- Port : 27017
- Stockage de données persistant utilisant un volume nommé
- Healthcheck configuré pour la fiabilité

### Mongo Express

- Nom du conteneur : `code-name-express`
- Image : mongo-express:1.0.2
- Port : 8080 (mappé sur le port 8081 dans le conteneur)
- Fournit une interface d'administration web pour MongoDB

## Configuration

Les variables d'environnement sont utilisées pour la configuration et doivent être définies dans un fichier `.env` :

| Variable d'environnement | Description |
|--------------------------|-------------|
| `MONGO_ROOT_USER` | Nom d'utilisateur root MongoDB |
| `MONGO_ROOT_PASSWORD` | Mot de passe root MongoDB |
| `MONGO_DATABASE_NAME` | Nom de la base de données MongoDB |
| `MONGO_EXPRESS_LOGIN` | Nom d'utilisateur pour Mongo Express |
| `MONGO_EXPRESS_PASSWORD` | Mot de passe pour Mongo Express |
| `MONGO_HOST` | Hôte de la base de données MongoDB |
| `MONGO_PORT` | Port de la base de données MongoDB |
| `SEEDER` | Active ou désactive l'insertion des données dans la base de données au lancement du serveur |
## Utilisation

1. Créez un fichier `.env` avec les variables d'environnement requises.
2. Exécutez la commande suivante pour démarrer tous les services :

   ```
   docker-compose up -d
   ```

3. Accédez à l'application web à l'adresse `http://localhost:8000`
4. Accédez à Mongo Express à l'adresse `http://localhost:8080`

## Réseaux

Tous les services sont connectés à un réseau personnalisé nommé `code-name`.

## Volumes

Un volume nommé `data` est utilisé pour persister les données MongoDB.

## Remarques

- Le code de l'application web doit se trouver dans le répertoire courant.
- Les données MongoDB sont persistantes entre les redémarrages des conteneurs.
- Mongo Express redémarre automatiquement en cas de crash.