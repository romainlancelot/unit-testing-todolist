<h1>CC de Tests Unitaires et Logiciels</h1>

Bonjour Monsieur, README pour vous dire comment installer tout ce qu'il faut pour run les tests :)

<h1>Tables des matières</h1>

- [Requirements](#requirements)
- [Installation](#installation)
- [Tests](#tests)

# Requirements

- Python 3.12

# Installation

Pour installer toutes les dépendances nécéssaires au projet, faites les commandes suivantes:
```bash
votre_machine@votre_distribution:~$ python -m venv venv
votre_machine@votre_distribution:~$ source venv/bin/activate # /venv/Scripts/activate sur Windows
(venv) votre_machine@votre_distribution:~$ pip install .

# Nécéssaire pour lancer les tests avec postman
(venv) votre_machine@votre_distribution:~$ python manage.py migrate
(venv) votre_machine@votre_distribution:~$ python manage.py runserver
```

Et c'est tout, vous pouvez donc lancez les tests !

# Tests

Pour lancer les tests, faite la commande suivante:

```bash
(venv) votre_machine@votre_distribution:~$ pytest
```

`pytest` par défaut, montre dans l'ordre:
- Les informations sur le système
- La liste des tests, et si ils ont réussi ou non
- Et pour finir, le nombre de tests réussis, échoués, et le temps total de test