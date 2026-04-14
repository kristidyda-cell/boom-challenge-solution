import argparse
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Generate inverse design submission CSV.")
    parser.add_argument("--model", default="models/forward_model.joblib", help="Path to trained model")
    parser.add_argument("--constraints", default="data/inverse_design/constraints.json", help="Path to constraints JSON")
    parser.add_argument("--train-dir", default="data/forward_prediction", help="Directory containing train.csv")
    parser.add_argument("--out", default="outputs/design_submission.csv", help="Output design CSV")
    parser.add_argument("--n-samples", type=int, default=250000, help="Random search sample count")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    args = parser.parse_args()

    model = joblib.load(args.model)
    train_dir = Path(args.train_dir)
    X_train = pd.read_csv(train_dir / "train.csv")
    with open(args.constraints) as f:
        cfg = json.load(f)

    bounds = cfg["input_bounds"]
    constraints = cfg["constraints"]
    feature_order = ["energy", "angle_rad", "coupling", "strength", "porosity", "gravity", "atmosphere", "shape_factor"]

    rng = np.random.default_rng(args.seed)
    samples = pd.DataFrame({
        name: rng.uniform(spec["min"], spec["max"], args.n_samples)
        for name, spec in bounds.items()
    })

    pred = pd.DataFrame(model.predict(samples[X_train.columns]), columns=["P80", "fines_frac", "oversize_frac", "R95", "R50_fines", "R50_oversize"])
    feasible = pred["P80"].between(constraints["p80_min"], constraints["p80_max"]) & (pred["R95"] <= constraints["r95_max"])

    cand = pd.concat([samples.loc[feasible].reset_index(drop=True), pred.loc[feasible].reset_index(drop=True)], axis=1)
    cand["objective"] = cand["energy"] + cand["R95"] / 200.0

    mins = np.array([bounds[k]["min"] for k in feature_order], float)
    maxs = np.array([bounds[k]["max"] for k in feature_order], float)

    selected = []
    for _, row in cand.sort_values(["objective", "energy", "R95"]).iterrows():
        x = row[feature_order].to_numpy(dtype=float)
        if not selected:
            selected.append(row)
        else:
            arr = np.vstack([s[feature_order].to_numpy(dtype=float) for s in selected])
            xn = (x - mins) / (maxs - mins)
            arrn = (arr - mins) / (maxs - mins)
            dmin = np.sqrt(((arrn - xn) ** 2).sum(axis=1)).min()
            if dmin > 0.18:
                selected.append(row)
        if len(selected) == 20:
            break

    if len(selected) < 20:
        raise RuntimeError(f"Only found {len(selected)} diverse feasible scenarios; increase --n-samples.")

    design = pd.DataFrame(selected)[feature_order].reset_index(drop=True)
    design.insert(0, "submission_id", np.arange(1, len(design) + 1, dtype=int))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    design.to_csv(out, index=False)
    print(f"Saved inverse design file to {out}")



if __name__ == "__main__":
    main()
