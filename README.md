# API REST : accéder à des données et des fonctionnalités via le web

Afin de suivre cet atelier, vous devrez vous assurer que le notebook `atelier.ipynb` puisse être ouvert.

## Via Google Colab (préférable)
Vous pouvez ouvrir le notebook via Google Colab, simplement en cliquant sur le badge suivant :
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ulaval-rs/prog-fest-web-workshop/blob/main/atelier.ipynb)


### Via Binder 
Vous pouvez ouvrir le notebook via Binder, simplement en cliquant sur le badge suivant :
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ulaval-rs/prog-fest-web-workshop/HEAD?labpath=atelier.ipynb)

### Via jupyter notebook (localement)
- Cloner le projet 
  ```shell
  git clone https://github.com/ulaval-rs/prog-fest-web-workshop
  cd prog-fest-web-workshop
  ```
- Installer les dépendances (`requests`, `pydicom`, `matplotlib`, `jupyter`)
  ```shell
  python -m venv venv
  ./venv/bin/pip install requests pydicom matplotlib jupyter
  ```
- Démarrer le jupyter notebook dans la racine du projet
  ```shell
  ./venv/bin/jupyter notebook
  ```
- Ouvrir `atelier.ipynb` dans l'interface de jupyter notebook


## Démarrer l'API REST localement
Cloner d'abord le projet et entrer dans celui-ci
```shell
git clone https://github.com/ulaval-rs/prog-fest-web-workshop
cd prog-fest-web-workshop
```
Créer un environement virtuel
```shell
python -m venv venv
./venv/bin/pip install -r requirements.txt
```
Finalement, démarrez l'application
```shell
./venv/bin/python app.py
```
L'application est désormais accessible à l'adresse `http://localhost:5000`.
