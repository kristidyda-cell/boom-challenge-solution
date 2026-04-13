# Simple Video Script

Hi, I am Khrystyna, and this submission is for the Boom: Trajectory Unknown Challenge.

For the forward prediction task, I treated the problem as tabular multi-output regression. The input consists of 8 impact parameters, and the outputs are 6 ejecta statistics. I trained an Extra Trees regressor because it handles nonlinear tabular relationships well, works reliably with limited preprocessing, and gave a strong validation baseline.

My workflow was:
1. Load the provided training inputs and labels
2. Train the model on the full training set
3. Run the provided test set through the trained model
4. Export the results in the required `prediction_submission.csv` format

For the inverse design task, I used the trained forward model as a surrogate evaluator. I sampled many candidate impact scenarios within the provided bounds, predicted their ejecta outcomes, filtered for candidates that satisfied the required P80 and R95 constraints, and then selected a diverse set of 20 feasible scenarios, favoring lower-energy and lower-range solutions.

I organized the solution as a reproducible repository with separate scripts for training, forward prediction, and inverse design, along with the generated submission files.

Thank you for reviewing my submission.
