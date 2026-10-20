# Tcl pour VLSI · De la Syntaxe de Base à l'Automatisation DRV

<p align="center">
  <a href="README.md">English</a> · 
  <a href="README.zh.md">简体中文</a> · 
  <a href="README.ms.md">Bahasa Melayu</a> · 
  <b>Français</b>
</p>

[![Licence : CC BY 4.0](https://img.shields.io/badge/Licence-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub](https://img.shields.io/badge/GitHub-SJTU--YONGFU--RESEARCH--GRP%2Ftcl--language-181717?logo=github)](https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language)
[![Bac à sable Web](https://img.shields.io/badge/Playground-Zéro--Installation-17776b?logo=javascript&logoColor=white)](https://sjtu-yongfu-research-grp.github.io/tcl-language/playground/)
[![DRV-Lite](https://img.shields.io/badge/DRV--Lite-Zéro--Licence_Simulateur_Layout-0f4f46)](docs/DRVLITE_HELP.md)
[![Labo STA](https://img.shields.io/badge/Labo_STA-Marge_Slack-b96b28)](docs/TIMING_ANALYZER_LAB.md)
[![Multilingue](https://img.shields.io/badge/i18n-EN%20%7C%20ZH%20%7C%20MS%20%7C%20FR-blue)](https://sjtu-yongfu-research-grp.github.io/tcl-language/fr/)

Plateforme pédagogique et pratique d'initiation au **Script Tcl pour VLSI**, conçue pour les débutants et couvrant la syntaxe moderne de Tcl, les structures de données, la programmation orientée objet (TclOO) et son utilisation concrète dans l'analyse de layout de circuits intégrés, les violations de règles de conception (DRV) et l'analyse temporelle statique (STA).

---

## 🌟 Fonctionnalités Clés & Outils Interactifs (Core Features)

Intégration d'outils open-source de pointe développés à l'Université Jiao Tong de Shanghai (SJTU) :

1. **⚡ Bac à Sable Web Interactif (Interactive Web Playground)** :
   - Zéro installation locale requise, exécution 100% dans le navigateur côté client sans dépendance de serveur distant.
   - Préchargé avec des modèles essentiels : modèle de substitution de Welch, expr sécurisé avec accolades, listes, dictionnaires, analyse STA et scripts DRV-Lite.
   - [👉 Lancer le Web Playground en ligne](https://sjtu-yongfu-research-grp.github.io/tcl-language/playground/)

2. **📐 DRV-Lite : Simulateur de Layout en Pur Tcl & Visualiseur en Ligne** :
   - Aucune licence commerciale EDA requise ! Modèle d'objets `layout` écrit en pur Tcl pour manipuler polygones, broches, couches et coordonnées de layout.
   - Accompagné d'un [📐 Visualiseur de Layout VLSI Interactif](https://sjtu-yongfu-research-grp.github.io/tcl-language/help/layout_viewer/), prenant en charge le zoom, le déplacement et l'exécution interactive de commandes Tcl de style CalibreDRV (`create`, `delete`, `bbox`, `iterator count`, `shift`, `scale`, etc.).

3. **⚡ Labo d'Analyse Temporelle STA & Contrôleur de Tapeout** :
   - Analyse de rapports temporels réels (`data/sample_timing.rpt`), calcul du Worst Negative Slack (WNS) et Total Negative Slack (TNS).
   - Accompagné du [⚡ Contrôleur Temporel STA Interactif](https://sjtu-yongfu-research-grp.github.io/tcl-language/help/timing_calculator/) permettant d'ajuster les périodes d'horloge, délais combinatoires et incertitudes pour valider les critères d'approbation de fabrication (tapeout).

4. **🎯 18 Exercices Pratiques de Données (54 Tâches Échelonnées) & Solutions** :
   - Couvre la substitution de variables, le tri de listes, dictionnaires imbriqués, expressions régulières, analyse de fichiers, conversions CSV/JSON et agrégations multicritères.
   - Basé sur des jeux de données d'ingénierie réels : `data/chip_runs.csv`, `data/top10_servers.tsv`, `data/wafers.csv`, `data/weather_beijing.json`, etc.
   - Modèles de départ (`exercises/`) et solutions complètes de référence (`solutions/`).

5. **🏆 6 Projets Capstone d'Ingénierie de Données (Projets A–F)** :
   - **Projet A** : Statistiques de journaux d'accès Nginx/Apache & filtrage d'alertes
   - **Projet B** : Agrégation de rendement de test de plaquettes (wafers) & classification de défauts
   - **Projet C** : Génération de rapports de métriques d'historique de commits Git
   - **Projet D** : Rapprochement automatisé des flux de ventes et d'inventaire
   - **Projet E** : Pipeline de nettoyage & conversion multiformat JSON/CSV
   - **Projet F** : Analyse de rapports textuels EDA & audit des violations de layout DRV
   - Fourni avec des suites de cas de test d'assertion (`case-1.tcl` à `case-4.tcl`).

6. **🧠 Modèle Mental Tcl en 3 Étapes** :
   - Respect strict du cycle `Regroupement (Grouping)` $\to$ `Substitution` $\to$ `Évaluation (Invocation)` pour comprendre la distinction fondamentale entre accolades `{}` et guillemets `""`, ainsi que la bonne pratique `expr {$a + $b}`.

7. **🎯 Défi Quiz & Tableau d'Honneur Public** :
   - 4 modules d'évaluation avec émission de certificats numériques vérifiables et classement communautaire en direct.

---

## 📚 Programme d'Études (40 Leçons) (Curriculum Roadmap)

- **M10 : Syntaxe de Base Tcl (Leçons 01–10)** : Commandes fondamentales, variables, structures de contrôle, procédures `proc`, listes et modèle mental en trois étapes.
- **M20 : Fluidité & Programmation Orientée Objet (Leçons 11–20)** : Dictionnaires `dict`, E/S de fichiers, expressions régulières (regex), espaces de noms `namespace` et `TclOO`.
- **M30 : Cœur de Layout Calibre (Leçons 21–30)** : Simulateur de layout en pur Tcl DRV-Lite, création de couches, polygones géométriques et commandes CalibreDRV.
- **M40 : Catalogue Layout & Validation Industrielle (Leçons 31–40)** : Analyse temporelle STA, extraction DEF/LEF, audit des violations DRV et flux de correction automatisée ECO.

---

## 🚀 Démarrage Rapide (Quick Start)

### 1. Prérequis Environnement
- **Leçons 1–20** : Installer [`tclsh`](https://www.tcl.tk/) dans votre terminal local (Tcl 8.5/8.6/9.0).
- **Leçons 21–40** : `calibredrv` commercial **ou** le simulateur en pur Tcl **DRV-Lite** (basculement automatique sans configuration requise).

### 2. Clonage & Commandes Fréquentes

```bash
git clone https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language.git
cd tcl-language

# Vérifier l'environnement local & l'état de DRV-Lite
make check-env

# Lancer les 6 tests unitaires du simulateur DRV-Lite
make drvlite-test

# Lancer le labo d'analyse temporelle STA
make timing-demo

# Exécuter le premier exemple de la Leçon 1
make week1-01

# Exécuter le script de layout de la Leçon 21 (simulation DRV-Lite)
make week21-01

# Exécuter les solutions d'exercices et les tests de projets capstone
tclsh solutions/01/01.tcl
(cd capstone/A && tclsh solution.tcl)
```

### 3. Compilation du Site Documentaire

```bash
make site-install    # Installer les dépendances Python & MkDocs
make site            # Générer la documentation statique et le site multilingue
make site-serve      # Prévisualisation locale sur http://127.0.0.1:8000
```

---

## 📁 Organisation du Dépôt (Repository Layout)

```text
tcl-language/
├── PLAN.md                 # Programme d'études sur 40 semaines & progression
├── Makefile                # Lanceur de cours, tests unitaires & compilation du site
├── data/                   # Jeux de données industriels réels (plaquettes, logs, STA)
├── exercises/              # 18 modèles de départ d'exercices (54 tâches)
├── solutions/              # 18 solutions de référence standardisées
├── capstone/               # 6 projets d'ingénierie de données (A–F avec tests)
├── homework/               # Devoirs et validateurs automatisés
├── quiz/                   # Banque de quiz et défis d'évaluation
├── lessons/                # 40 leçons bilingues & 100+ scripts d'exemples exécutables
├── examples/               # Exemples industriels tels que timing_report_analyzer.tcl
├── docs/                   # Guides de référence TCL_HELP.md, DRVLITE_HELP.md
├── tools/
│   ├── drvlite/            # Simulateur de layout Calibre DESIGNrev en pur Tcl
│   └── ...                 # Outils d'inspection syntaxique et de commandes
└── website/                # Fichiers sources MkDocs & documentation multilingue
```

---

## 👥 Contributeurs & Attribution (Contributors)

Remerciements chaleureux aux membres de l'équipe de recherche, aux enseignants et aux étudiants contributeurs (par ordre alphabétique des identifiants GitHub) :

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/yongfu-li">
        <img src="https://avatars.githubusercontent.com/u/10367890?v=4" width="80" height="80" alt="yongfu-li"/><br/>
        <sub><b>Li Yongfu</b></sub><br/>
        <sub>@yongfu-li</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Capeur">
        <img src="https://avatars.githubusercontent.com/u/197603203?v=4" width="80" height="80" alt="Capeur"/><br/>
        <sub><b>David MUY</b></sub><br/>
        <sub>@Capeur</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/FanqinZeng">
        <img src="https://avatars.githubusercontent.com/u/151010024?v=4" width="80" height="80" alt="FanqinZeng"/><br/>
        <sub><b>FanQin Zeng</b></sub><br/>
        <sub>@FanqinZeng (WASM & Exercises)</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/GateUltra">
        <img src="https://avatars.githubusercontent.com/u/138369042?v=4" width="80" height="80" alt="GateUltra"/><br/>
        <sub><b>GateUltra</b></sub><br/>
        <sub>@GateUltra (Homeworks)</sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/muranfei">
        <img src="https://avatars.githubusercontent.com/u/31174606?v=4" width="80" height="80" alt="muranfei"/><br/>
        <sub><b>muranfei</b></sub><br/>
        <sub>@muranfei</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/stephQ-lab">
        <img src="https://avatars.githubusercontent.com/u/186373504?v=4" width="80" height="80" alt="stephQ-lab"/><br/>
        <sub><b>stephQ-lab</b></sub><br/>
        <sub>@stephQ-lab</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Su3037">
        <img src="https://avatars.githubusercontent.com/u/154591477?v=4" width="80" height="80" alt="Su3037"/><br/>
        <sub><b>Supan</b></sub><br/>
        <sub>@Su3037</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/thy031">
        <img src="https://avatars.githubusercontent.com/u/188567228?v=4" width="80" height="80" alt="thy031"/><br/>
        <sub><b>thy031</b></sub><br/>
        <sub>@thy031 (Quizzes)</sub>
      </a>
    </td>
  </tr>
</table>

Consultez [`CONTRIBUTORS.md`](CONTRIBUTORS.md) et la [Liste des Contributeurs](https://sjtu-yongfu-research-grp.github.io/tcl-language/fr/contributors/) en ligne.

---

## 📜 Licence (License)

- Le contenu des cours et de la documentation est sous licence [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- Le code source des scripts et outils de simulation est sous licence [MIT License](LICENSE).
