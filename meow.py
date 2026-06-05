import os
from src.log import log
from src.dl import MeowDataLoader
from src.feat import MeowFeatureGenerator
from src.mdl import MeowModel
from src.eval import MeowEvaluator
from src.tradingcalendar import Calendar


class MeowEngine(object):
    def __init__(self, h5dir, cacheDir):
        self.calendar = Calendar()
        self.h5dir = h5dir
        if not os.path.exists(h5dir):
            raise ValueError("Data directory not exists: {}".format(self.h5dir))
        if not os.path.isdir(h5dir):
            raise ValueError("Invalid data directory: {}".format(self.h5dir))
        self.cacheDir = cacheDir # this is not used in sample code
        self.dloader = MeowDataLoader(h5dir=h5dir)
        self.featGenerator = MeowFeatureGenerator(cacheDir=cacheDir)
        self.model = MeowModel(cacheDir=cacheDir)
        self.evaluator = MeowEvaluator(cacheDir=cacheDir)

    def fit(self, startDate, endDate):
        dates = self.calendar.range(startDate, endDate)
        rawData = self.dloader.loadDates(dates)
        log.inf("Running model fitting...")
        xdf, ydf = self.featGenerator.genFeatures(rawData)
        self.model.fit(xdf, ydf)

    def predict(self, xdf):
        return self.model.predict(xdf)

    def eval(self, startDate, endDate):
        log.inf("Running model evaluation...")
        dates = self.calendar.range(startDate, endDate)
        rawData = self.dloader.loadDates(dates)
        xdf, ydf = self.featGenerator.genFeatures(rawData)
        ydf.loc[:, "forecast"] = self.predict(xdf)
        self.evaluator.eval(ydf)


if __name__ == "__main__":
    engine = MeowEngine(h5dir="./archive", cacheDir=None)

    # --- ResidualMLP ---
    if os.path.exists("model_weights.pt") and os.path.exists("scaler.pkl"):
        log.inf("Found saved ResidualMLP model, skipping training")
        engine.model.load("model_weights.pt", "scaler.pkl")
    else:
        engine.fit(20230601, 20231130)

    # --- LightGBM ---
    from src.mdl_lgb import MeowModelLGB
    lgbModel = MeowModelLGB()
    if os.path.exists("lgb_model.txt") and os.path.exists("lgb_scaler.pkl"):
        lgbModel.load("lgb_model.txt", "lgb_scaler.pkl")
    else:
        log.inf("Training LightGBM on training set...")
        trainDates = engine.calendar.range(20230601, 20231130)
        trainRawData = engine.dloader.loadDates(trainDates)
        trainXdf, trainYdf = engine.featGenerator.genFeatures(trainRawData)
        lgbModel.fit(trainXdf, trainYdf)

    # --- Ensemble evaluation ---
    evalDates = engine.calendar.range(20231201, 20231229)
    evalRawData = engine.dloader.loadDates(evalDates)
    xdf, ydf = engine.featGenerator.genFeatures(evalRawData)

    ydf["forecast_mlp"] = engine.model.predict(xdf)
    ydf["forecast_lgb"] = lgbModel.predict(xdf)
    ydf["forecast"] = (ydf["forecast_mlp"] + ydf["forecast_lgb"]) / 2

    engine.evaluator.eval(ydf)
