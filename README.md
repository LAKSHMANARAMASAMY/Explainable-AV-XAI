# Explainable AV XAI — Reference Implementation

This package accompanies the manuscript **“An Explainable IoT-Driven Framework for Trustworthy Decision-Making in Safety-Critical Autonomous Vehicles.”**

## Important reproducibility note

The manuscript states that 450 synthetic scenarios were generated, and this package separates:

1. `src/reproduce\_reported\_results.py` — recreates manuscript tables/plots from values reported in the paper. 
2. `src/run\_reference\_pipeline.py` — a transparent reference implementation consistent with the described methodology.

## Included

* 450 reference synthetic scenarios (90 per category)
* Decision Tree classification
* Linear Regression demonstration
* optional SHAP and LIME helpers
* TI, DTS, ARM, and CO helper functions
* scripts for Tables 3–5 and Figures 3–8 based on manuscript values

## Run

```bash
pip install -r requirements.txt
python src/reproduce\_reported\_results.py
python src/run\_reference\_pipeline.py
```

## Data sources cited by the manuscript

Lost and Found, Nexar Collision Prediction, nuScenes, CADC, TWICE digital twin dataset, and autonomous-vehicle ethics literature. Third-party datasets are not redistributed here.

