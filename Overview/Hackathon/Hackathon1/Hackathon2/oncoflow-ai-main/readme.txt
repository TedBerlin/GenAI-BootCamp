🏥 OncoFlow AI – Résumeur de recherches en oncologie

💡 OncoFlow AI est un pipeline léger basé sur des modèles de langage (LLM) pour extraire, résumer et analyser des études cliniques en oncologie à partir de fichiers PDF. Conçu pour fonctionner efficacement sur des CPU locaux – même sur un Raspberry Pi.

Fonctionnalités principales

Résumé multi-documents : Comparez plusieurs études cliniques côte à côte.
Détection d’erreurs : Détecte 5 types d’incohérences liées au dosage à l’aide de règles et de modèles ML légers.
Support LLM : Compatible avec phi-3-mini (via Ollama) et t5-small (via HuggingFace).
Optimisé CPU : Fonctionne même sur un Raspberry Pi 4 ou des machines à faibles ressources.
Technologies utilisées

Résumé : t5-small ou phi-3-mini (via Ollama)
Recherche multi-documents : FAISS-CPU et sentence-transformers
Détection d’erreurs : Règles hybrides + modèle léger
Extraction de texte : pypdf, spaCy
Interface utilisateur : Streamlit (interface web simple)
Démarrage rapide

Installer l’application Ollama (uniquement pour phi3)
Lien : https://ollama.com/download
Lancer le script (uniquement sur macOS)
./run_phi3.sh
ou
./run_t5.sh
OU

Cloner le dépôt
git clone https://github.com/your-org/oncoflow-ai.git
cd oncoflow-ai
Créer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate (Sur Windows : .venv\Scripts\activate)
Installer les dépendances
Pour la version phi-3-mini :
pip install -r requirements-phi3.txt
Pour la version t5-small :
pip install -r requirements-t5.txt
Lancer en ligne de commande
Mode document unique :
python phi3_ollama/pipeline_phi3.py --input=pdfs/mon_etude.pdf
Mode multi-documents :
python phi3_ollama/pipeline_phi3.py --input=pdfs/ --multi
Lancer l’interface web (Streamlit)
Structure du projet

oncoflow-ai/

phi3_ollama/
summarizer_core_phi3.py
streamlit_phi3.py
evaluate_phi3.py
t5_pipeline/
summarizer_core_t5.py
streamlit_t5.py
evaluate_t5.py
shared/
pdf_extract.py
semantic_filter.py
utils.py
data/
test_set.json
requirements-phi3.txt
requirements-t5.txt
run_phi3.sh
Exemple de consigne (dans l’interface Streamlit)

Concentre-toi sur les stratégies de traitement pour le cancer du sein triple négatif. Donne-moi un résumé comparatif de 100 mots.

Évaluation des performances

Version t5-pipeline :

BLEU moyen : 11.21
ROUGE-1 : 0.41
ROUGE-2 : 0.15
ROUGE-L : 0.28
Perplexité : 110.73
Version phi3-ollama :

BLEU moyen : 0.51
ROUGE-1 : 0.06
ROUGE-2 : 0.01
ROUGE-L : 0.06
Perplexité : 54.64