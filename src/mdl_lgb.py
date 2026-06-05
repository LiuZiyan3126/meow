import pickle
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
from src.log import log


class MeowModelLGB(object):
    def __init__(self, cacheDir=None):
        self.cacheDir = cacheDir
        self.scaler = StandardScaler()
        self.model = None
        self.valFraction = 0.15
        self.earlyStoppingRounds = 50
        self.params = {
            'objective': 'regression',
            'metric': 'rmse',
            'num_leaves': 127,
            'learning_rate': 0.05,
            'feature_fraction': 0.8,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'min_data_in_leaf': 100,
            'verbose': -1,
            'seed': 42,
        }

    def fit(self, xdf, ydf):
        X = xdf.to_numpy().astype(np.float32)
        y = ydf.to_numpy().astype(np.float32).ravel()

        n = len(X)
        nVal = int(n * self.valFraction)
        XTrain, XVal = X[:-nVal], X[-nVal:]
        yTrain, yVal = y[:-nVal], y[-nVal:]

        XTrain = self.scaler.fit_transform(XTrain)
        XVal = self.scaler.transform(XVal)

        trainData = lgb.Dataset(XTrain, label=yTrain)
        valData = lgb.Dataset(XVal, label=yVal, reference=trainData)

        log.inf("Training LightGBM with {} samples, {} features...".format(len(XTrain), XTrain.shape[1]))
        self.model = lgb.train(
            self.params,
            trainData,
            num_boost_round=5000,
            valid_sets=[trainData, valData],
            valid_names=['train', 'val'],
            callbacks=[
                lgb.early_stopping(self.earlyStoppingRounds),
                lgb.log_evaluation(50),
            ],
        )

        bestIter = self.model.best_iteration
        bestScore = self.model.best_score['val']['rmse']
        log.inf("Done fitting: best_iteration={}, best_val_rmse={:.6f}".format(bestIter, bestScore))

        self.model.save_model("lgb_model.txt")
        with open("lgb_scaler.pkl", "wb") as f:
            pickle.dump(self.scaler, f)
        log.inf("Model saved to lgb_model.txt, scaler saved to lgb_scaler.pkl")

    def load(self, modelPath="lgb_model.txt", scalerPath="lgb_scaler.pkl"):
        self.model = lgb.Booster(model_file=modelPath)
        with open(scalerPath, "rb") as f:
            self.scaler = pickle.load(f)
        log.inf("LightGBM model loaded from {} and {}".format(modelPath, scalerPath))

    def predict(self, xdf):
        X = self.scaler.transform(xdf.to_numpy().astype(np.float32))
        return self.model.predict(X)
