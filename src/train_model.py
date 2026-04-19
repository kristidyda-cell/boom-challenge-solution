import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor


def main():
    parser = argparse.ArgumentParser(description="Train the forward prediction model for the Boom challenge.")
    parser.add_argument("--data-dir", default="data/forward_prediction", help="Directory containing train.csv and train_labels.csv")
    parser.add_argument("--model-out", default="models/forward_model.joblib", help="Path to write the trained model")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    X = pd.read_csv(data_dir / "train.csv")
    y = pd.read_csv(data_dir / "train_labels.csv")

    model = ExtraTreesRegressor(
        n_estimators=800,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=1,
    )
    model.fit(X, y)

    model_out = Path(args.model_out)
    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_out)
    print(f"Saved model to {model_out}")


if __name__ == "__main__":
    main()
