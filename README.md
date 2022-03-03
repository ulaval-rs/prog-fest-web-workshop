# API REST : accéder à des données et des fonctionnalités via le web

Afin de suivre cet atelier, vous devrez vous assurer que le notebook `atelier.ipynb` puisse être ouvert.

### Via Binder (préférable)
Vous pouvez ouvrir le notebook via Binder, simplement en cliquant sur le badge suivant :
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ulaval-rs/prog-fest-web-workshop/HEAD?labpath=atelier.pynb)

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
