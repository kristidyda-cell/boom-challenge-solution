import argparse
from pathlib import Path
import joblib
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Generate forward prediction submission CSV.")
    parser.add_argument("--model", default="models/forward_model.joblib", help="Path to trained model")
    parser.add_argument("--data-dir", default="data/forward_prediction", help="Directory containing train_labels.csv and test.csv")
    parser.add_argument("--out", default="outputs/prediction_submission.csv", help="Output submission CSV path")
    args = parser.parse_args()

    model = joblib.load(args.model)
    data_dir = Path(args.data_dir)
    train_labels = pd.read_csv(data_dir / "train_labels.csv")
    X_test = pd.read_csv(data_dir / "test.csv")

    pred = pd.DataFrame(model.predict(X_test), columns=train_labels.columns)
    for col in train_labels.columns:
        pred[col] = pred[col].clip(train_labels[col].min(), train_labels[col].max())

    pred.insert(0, "scenario_id", np.arange(len(pred), dtype=int))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pred.to_csv(out, index=False)
    print(f"Saved predictions to {out}")


if __name__ == "__main__":
    main()
