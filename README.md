# Classification Automatique des Stades de Sommeil à Partir d'un EEG

# Introduction

Dans ce projet, j'utilise des enregistrements EEG (électroencéphalogramme) pour annoter automatiquement les stades de sommeil. Je travaille avec le jeu de données Physionet Sleep-EDF de 2018, qui comprend 153 enregistrements de sommeil complets d'environ 20 heures, contenant des signaux EEG, EOG (électrooculogramme) et EMG (électromyogramme). Ces signaux sont essentiels pour diagnostiquer des troubles du sommeil tels que l'apnée du sommeil et l'hypersomnie.

# Objectif

L'interprétation manuelle des signaux EEG pour classifier les stades de sommeil est laborieuse et chronophage. Mon objectif est de développer un modèle de deep learning capable de classer ces stades automatiquement.

# Méthodologie

Mon modèle s'inspire de deux études :

    SleepEEGNet : Cette méthode utilise des réseaux de neurones convolutifs (CNN) et un modèle séquence-à-séquence, combinant attention et réseaux de neurones récurrents bidirectionnels, offrant une grande précision dans l'annotation des stades de sommeil. [1]

    CNN : Dans cette étude, les auteurs ont montré que les CNN pouvaient apprendre de manière autonome à distinguer les différents stades de sommeil sans connaissances préalables. [2]

Bien que mon approche ne reproduise pas intégralement la première méthode, elle suit un processus similaire et met en lumière les défis rencontrés lors de l'application de méthodes de recherche complexes. Cela m'aide à comprendre l'application des concepts de deep learning dans des situations réelles.

# Résultats

J'ai évalué ma méthode sur plusieurs canaux EEG (Fpz-Cz et Pz-Oz) des ensembles de données Sleep-EDF, obtenant une précision globale de 83,7 % et un score macro F1 de 60,17 %. Pour atténuer le problème de déséquilibre des classes dans les données de sommeil, j'ai appliqué une pondération des classes.

# Mots-clés

Annotation de stades de sommeil, analyse EEG, deep learning, réseaux de neurones convolutifs.

# Sources

[1]	Mousavi, Sajad, Fatemeh Afghah, et U. Rajendra Acharya. " SleepEEGNet: Automated Sleep Stage Scoring with Sequence to Sequence Deep Learning Approach ". PLOS ONE 14, n? 5 (7 mai 2019): e0216456. https://doi.org/10.1371/journal.pone.0216456
[2]	Tsinalis, Orestis, Paul M. Matthews, Yike Guo, et Stefanos Zafeiriou. « Automatic Sleep Stage Scoring with Single-Channel EEG Using Convolutional Neural Networks ». arXiv, 5 octobre 2016. https://doi.org/10.48550/arXiv.1610.01683.

