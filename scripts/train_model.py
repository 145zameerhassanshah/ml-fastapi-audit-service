from pathlib import Path
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_SEED=42
MODEL_PATH=Path(__file__).resolve().parent.parent/'model'/'risk_model.joblib'

def build_training_data(n_samples=1200):
    rng=np.random.default_rng(RANDOM_SEED)
    age=rng.integers(18,91,n_samples); systolic=rng.integers(85,201,n_samples); diastolic=rng.integers(50,121,n_samples); glucose=rng.uniform(65,250,n_samples); bmi=rng.uniform(17,45,n_samples)
    latent=0.025*(age-45)+0.035*(systolic-120)+0.020*(diastolic-80)+0.018*(glucose-100)+0.090*(bmi-25)+rng.normal(0,1.5,n_samples)
    y=(latent>2.2).astype(int)
    X=np.column_stack([age,systolic,diastolic,glucose,bmi])
    return X,y

def main():
    X,y=build_training_data()
    model=Pipeline([('scaler',StandardScaler()),('classifier',LogisticRegression(max_iter=1000,random_state=RANDOM_SEED))])
    model.fit(X,y); MODEL_PATH.parent.mkdir(parents=True,exist_ok=True); joblib.dump(model,MODEL_PATH)
    print(f'Model saved to: {MODEL_PATH}'); print(f'Training samples: {len(X)}'); print(f'Class 1 prevalence: {y.mean():.3f}')

if __name__=='__main__': main()
