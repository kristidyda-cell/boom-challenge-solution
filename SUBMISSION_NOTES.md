# Submission Notes

## Files ready now
- `outputs/prediction_submission.csv` — mandatory forward prediction file
- `outputs/design_submission.csv` — optional inverse design file
- `models/forward_model.joblib` — trained model artifact

## What I can truthfully say

I have:
- a GitHub-ready repository structure
- a generated `prediction_submission.csv`
- a generated `design_submission.csv`
- a clear, reproducible method I can explain

## Method explanation in plain language

I trained a tree-based ensemble regressor on the provided impact-parameter dataset to predict all ejecta outcomes together. I chose Extra Trees because the challenge data is tabular, nonlinear, and likely contains interactions between physical parameters such as energy, gravity, angle, coupling, and material properties. This model gives a strong baseline with little preprocessing and good stability.
For inverse design, I used the trained forward model as a surrogate predictor. I randomly searched the allowed parameter ranges, kept only scenarios predicted to satisfy the contest constraints, and selected a diverse set of 20 low-impact candidates.

## What still must be done manually

- Create a real GitHub repository and upload these files
- Record the required submission video
- Submit through Freelancer's challenge interface
