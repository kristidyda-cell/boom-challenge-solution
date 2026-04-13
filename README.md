# Boom Challenge Submission Starter

This repository is a complete, reproducible starter submission for the **Boom: Trajectory Unknown Challenge**.

## What is included

- A trained **Extra Trees** multi-output regressor for forward prediction
- A generated `prediction_submission.csv`
- A generated `design_submission.csv`
- Scripts to retrain the model and regenerate both submission files
- A short explanation of the method and how to present it in your submission video

## Repository structure

```text
data/
  forward_prediction/
  inverse_design/
models/
  forward_model.joblib
outputs/
  prediction_submission.csv
  design_submission.csv
  design_candidates_with_predicted_outcomes.csv
src/
  train_model.py
  predict_forward.py
  generate_inverse_design.py
requirements.txt
SUBMISSION_NOTES.md
VIDEO_SCRIPT.md
```

## Approach summary

### Forward prediction
I framed the mandatory task as a **tabular multi-output regression** problem:

- Inputs: 8 impact parameters
- Outputs: 6 ejecta statistics

I used an **ExtraTreesRegressor** because it handles nonlinear tabular relationships well, is robust with mixed scales, and gives a strong baseline quickly without requiring extensive feature normalization.

Model settings:
- `n_estimators=800`
- `random_state=42`
- `n_jobs=-1`

A quick validation run gave a strong average R² around **0.92**, which is a good baseline for this dataset.

### Inverse design
For the optional inverse design task, I used the trained forward model as a fast surrogate evaluator:

1. Randomly sample many candidate impact scenarios inside the allowed bounds
2. Predict outcomes with the trained model
3. Keep only candidates satisfying:
   - `96 <= P80 <= 101`
   - `R95 <= 175`
4. Rank feasible points by a simple low-impact proxy favoring:
   - lower energy
   - lower R95
5. Apply a lightweight diversity filter so the 20 submitted scenarios are not near-duplicates

This gives a practical engineering solution that is easy to explain and reproduce.

## How to run

Create an environment and install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python src/train_model.py
```

Generate the mandatory forward submission:

```bash
python src/predict_forward.py
```

Generate the optional inverse design submission:

```bash
python src/generate_inverse_design.py
```

## What to upload

You still need to do these manual steps before final contest submission:

1. Push this folder to a **GitHub repository**
2. Record a short **video explanation**
3. Share the GitHub repo with `challenges@freelancer.com`
4. Upload:
   - `prediction_submission.csv`
   - optional `design_submission.csv`
   - your video
   - any required submission form fields

## Important note

This is a solid **baseline submission**, not a guarantee of winning. Before submitting, you should still:
- sanity-check the CSV formats
- confirm the GitHub repo is public or shared as required
- make sure your video clearly explains the method
