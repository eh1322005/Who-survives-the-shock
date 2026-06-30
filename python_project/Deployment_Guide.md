# Deployment Guide

## 1. Environment Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`xgboost`, `lightgbm`, `catboost`, and `shap` are optional. If `pip install`
fails for one of these on your platform, remove that line from
`requirements.txt` and reinstall — the notebook and app both detect missing
libraries and skip them automatically.

## 2. Generate the Model Artifacts

The Streamlit app and CLI script both expect a trained model under
`artifacts/`. Generate it by running the notebook fully, top to bottom:

```bash
jupyter nbconvert --to notebook --execute --inplace Global_Resilience_Final.ipynb
```

This produces:
- `artifacts/resilience_model_latest.joblib`
- `artifacts/resilience_model_latest.pkl`
- `artifacts/model_metadata.json`

Confirm they exist:

```bash
ls artifacts/
```

## 3. Configure Paths (Optional)

By default, `config.py` looks for the model in `./artifacts/` relative to
itself. To point at a different location (e.g., a shared model registry),
set an environment variable instead of editing the code:

```bash
export RESILIENCE_MODEL_PATH=/path/to/your/resilience_model_latest.joblib
```

## 4. Run the Streamlit App

```bash
streamlit run app.py
```

By default this opens at `http://localhost:8501`. To run on a specific port
(useful behind a reverse proxy):

```bash
streamlit run app.py --server.port 8080
```

## 5. Run Predictions from the Command Line

```bash
python predict.py \
    --digital 0.6 --economic 0.5 --food 0.7 \
    --healthcare 0.65 --political 0.55 --climate 0.6 \
    --region "Europe & Central Asia"
```

Run `python predict.py --help` to see the full flag list (it's generated
dynamically from the model's saved feature list, so it always matches the
currently deployed model).

## 6. Logging

All three entry points (`app.py`, `predict.py`, and the notebook's MLOps
section) log to `logs/app.log` as well as the console. Set the verbosity
with:

```bash
export RESILIENCE_LOG_LEVEL=DEBUG
```

## 7. Common Issues

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ModelLoadError: No model artifact found` | Notebook Section 11 hasn't been run yet | Re-run the notebook end-to-end |
| `Region 'X' was not seen during training` | Typo, or a region missing from the training data | Check `artifacts/model_metadata.json` → `regions` for valid values |
| App shows old model after retraining | Streamlit's `@st.cache_resource` cache is stale | Click the "⋮" menu → "Clear cache", or restart the app |
| `ImportError` for xgboost/lightgbm/catboost | Optional dependency not installed | Safe to ignore — the pipeline trains on the remaining models |

## 8. Re-deploying After Retraining

Every notebook run overwrites `resilience_model_latest.joblib` /
`.pkl` / `model_metadata.json` in place, and also writes a timestamped copy
(`resilience_model_<TIMESTAMP>.joblib`) for version history. The app always
reads the `_latest` files, so no code changes are needed after retraining —
just restart the Streamlit process (or clear its cache) to pick up the new
model.
