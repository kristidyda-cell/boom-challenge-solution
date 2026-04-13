# Boom Challenge Solution

This repository contains my submission for the Boom: Trajectory Unknown Challenge.

## Approach

The solution is built as a reproducible baseline for the two challenge tasks:

1. **Forward Prediction**  
   Train a supervised multi-output regression model on the provided impact simulation dataset and predict ejecta outcome variables for the test scenarios.

2. **Inverse Design**  
   Use the trained forward surrogate model to search for impact parameter combinations that satisfy the required ejecta constraints.

## Method Summary

For forward prediction, I used a tree-based ensemble regression approach that is well-suited for structured tabular data, nonlinear interactions, and multi-target prediction.  
The workflow includes:

- loading and validating the provided training and test files
- fitting a multi-output regression model on the training set
- generating predictions for the hidden test scenarios
- exporting results in the required submission format

For inverse design, I used bounded search guided by the trained forward model to identify candidate scenarios predicted to satisfy:

- `96 <= P80 <= 101`
- `R95 <= 175`

## Repository Contents

- `src/` - core scripts
- `outputs/` - generated submission files
- `README.md` - project overview and usage
- `SUBMISSION_NOTES.md` - concise technical notes
- `VIDEO_SCRIPT.md` - short explanation script for submission video

## Notes

This submission is designed as a clean, reproducible engineering baseline with emphasis on clarity, stability, and practical generalization on tabular simulation data.