# 📘 Documentation Technique : Compression d'Image via Décomposition QR

## 📝 Vue d'ensemble
Ce projet est une application Web interactive développée en **Python** avec **Streamlit**. Elle a pour but la démonstration pédagogique de la compression d'image en utilisant l'algèbre linéaire, spécifiquement la **Décomposition QR avec Pivot (Rank-Revealing QR)**.

L'application permet aux utilisateurs de visualiser comment une image peut être reconstruite approximativement en ne conservant que ses composantes mathématiques les plus significatives.

## 🚀 Installation

### Prérequis
- Python 3.8 ou version ultérieure.
- Pip (gestionnaire de paquets Python).

### Étape 1 : Installation des dépendances
Ouvrez un terminal à la racine du projet et exécutez :

```bash
pip install -r requirements.txt
```

*Les dépendances principales sont :*
- `streamlit` : Pour l'interface Web.
- `numpy` & `scipy` : Pour les calculs matriciels avancés.
- `Pillow` : Pour le traitement d'image.
- `matplotlib` : Pour l'affichage (optionnel, utilisé par Streamlit).

## 💻 Utilisation

### Lancement de l'application
Exécutez la commande suivante dans votre terminal :

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut (adresse locale : `http://localhost:8501`).

### Guide de l'Interface
1.  **Upload** : Utilisez la barre latérale gauche pour charger une image (format JPG ou PNG).
2.  **Conversion** : L'image est automatiquement convertie en niveaux de gris pour le traitement.
3.  **Réglage (Slider)** : Ajustez le curseur **"Nombre de composantes (k)"**.
    *   Un `k` faible donne une compression élevée mais une qualité moindre.
    *   Un `k` élevé améliore la qualité mais réduit le taux de compression.
4.  **Analyse** : Observez les résultats en temps réel sur le panneau principal (Image originale vs Compressée) et les métriques de performance.

## 🧠 Fonctionnement Technique

### Pourquoi la Décomposition QR ?
La décomposition QR est une méthode de factorisation de matrice. Pour une image représentée par une matrice $A$ de taille $m \times n$, on cherche à l'approcher par le produit de deux matrices plus petites.

### L'Algorithme : QR avec Pivot (Pivoted QR)
Initialement, la décomposition QR standard traite les colonnes de gauche à droite. Pour une image, cela signifie que les premières colonnes (gauche de l'image) sont privilégiées, ce qui est mauvais pour la compression globale.

Nous utilisons donc la **QR avec Pivot (Rank-Revealing QR)** implémentée via `scipy.linalg.qr`.

**Formule Mathématique :**
$$ A E = Q R $$

Où :
*   $A$ : Matrice de l'image originale.
*   $E$ : Matrice de permutation (re-ordonne les colonnes pour mettre les plus "importantes" en premier).
*   $Q$ : Matrice orthogonale ($m \times m$).
*   $R$ : Matrice triangulaire supérieure ($m \times n$) dont les éléments diagonaux sont décroissants (en valeur absolue).

**Processus de Compression :**
1.  On calcule $Q, R, P$ (permutation).
2.  On tronque les matrices pour ne garder que les $k$ premières colonnes de $Q$ et les $k$ premières lignes de $R$.
3.  On reconstruit l'image permutée : $B \approx Q_k \times R_k$.
4.  On inverse la permutation pour retrouver l'image finale correctement ordonnée.

Ce procédé garantit que nous conservons les vecteurs qui contribuent le plus à l'énergie globale de l'image, offrant une bien meilleure approximation visuelle pour un faible $k$.

## 📂 Structure du Code

- **`app.py`** : Point d'entrée de l'application. Gère l'interface utilisateur (UI), les callbacks Streamlit et l'affichage.
- **`qr_logic.py`** : Contient la logique métier pure (`compress_image`). C'est ici que l'algorithme `scipy.linalg.qr` est appelé et que la reconstruction des matrices est effectuée.
- **`requirements.txt`** : Liste des bibliothèques nécessaires.

---

