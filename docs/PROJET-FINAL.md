# Projet final — chapitre 13

Une application multi-services vous est livree. Elle fonctionne sur le poste du
developpeur. Rendez-la prete pour la production.

## Cinq jalons evalues

| Jalon | Contenu | Poids |
|---|---|---|
| 1 | Images construites, optimisees, publiees ; contrat de conteneur respecte | 15 % |
| 2 | Pile Compose fonctionnelle, donnees persistantes | 15 % |
| 3 | Deploiement Kubernetes : Deployments, Services, Ingress + TLS, config et secrets | 25 % |
| 4 | Production : probes, ressources, autoscaling, observabilite, securite | 25 % |
| 5 | CI/CD complet et revue d'architecture | 20 % |

## Livrables

- Le depot, avec son historique — la progression compte autant que l'etat final
- Les manifestes et le chart Helm
- Un tableau de bord repondant a une question precise, pas affichant tout
- Un document d'architecture de 4 pages
- Une soutenance de 20 minutes

## Revue d'architecture

Ce n'est pas une presentation du travail : c'est une **justification**. Pour
chaque decision, on attend la contrepartie. Trois questions seront posees :

1. Quel est le point de defaillance unique qui subsiste, et pourquoi
   l'avez-vous accepte ?
2. Qu'avez-vous choisi de ne PAS faire, et a quel cout auriez-vous pu le faire ?
3. Que se passe-t-il si le trafic est multiplie par dix demain matin ?

## Bareme

Fonctionnement 40 % — qualite technique 30 % — revue d'architecture 30 %.
La grille detaillee figure dans le fascicule des corriges, annexe E2.
