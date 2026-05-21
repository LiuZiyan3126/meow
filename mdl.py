import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from log import log
from nn_model import ResidualMLP, device


class MeowModel(object):
    def __init__(self, cacheDir):
        self.cacheDir = cacheDir
        self.scaler = StandardScaler()
        self.model = None
        self.batchSize = 8192
        self.lr = 1e-3
        self.weightDecay = 1e-4
        self.maxEpochs = 200
        self.patience = 25
        self.valFraction = 0.15

    def fit(self, xdf, ydf):
        X = xdf.to_numpy().astype(np.float32)
        y = ydf.to_numpy().astype(np.float32).ravel()

        n = len(X)
        nVal = int(n * self.valFraction)
        XTrain, XVal = X[:-nVal], X[-nVal:]
        yTrain, yVal = y[:-nVal], y[-nVal:]

        XTrain = self.scaler.fit_transform(XTrain)
        XVal = self.scaler.transform(XVal)

        XTrainT = torch.tensor(XTrain, dtype=torch.float32)
        yTrainT = torch.tensor(yTrain, dtype=torch.float32)
        XValT = torch.tensor(XVal, dtype=torch.float32)
        yValT = torch.tensor(yVal, dtype=torch.float32)

        inputDim = XTrain.shape[1]
        self.model = ResidualMLP(input_dim=inputDim).to(device)
        optimizer = optim.AdamW(self.model.parameters(), lr=self.lr, weight_decay=self.weightDecay)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10)
        lossFn = nn.MSELoss()
        targetScale = 100.0

        bestValLoss = float('inf')
        bestState = None
        patienceCounter = 0
        nTrain = len(XTrainT)
        nBatches = (nTrain + self.batchSize - 1) // self.batchSize

        for epoch in range(self.maxEpochs):
            self.model.train()
            perm = torch.randperm(nTrain)
            epochLoss = 0.0
            batchesDone = 0
            for i in range(nBatches):
                start = i * self.batchSize
                end = min(start + self.batchSize, nTrain)
                if end - start < 2:
                    continue
                idx = perm[start:end]
                Xb = XTrainT[idx].to(device)
                yb = yTrainT[idx].to(device)
                optimizer.zero_grad()
                pred = self.model(Xb)
                loss = lossFn(pred, yb * targetScale)
                loss.backward()
                optimizer.step()
                epochLoss += loss.item()
                batchesDone += 1
            epochLoss /= max(batchesDone, 1)

            self.model.eval()
            with torch.no_grad():
                valPred = self.model(XValT.to(device))
                valLoss = lossFn(valPred, yValT.to(device) * targetScale).item()

            scheduler.step(valLoss)

            if epoch % 5 == 0:
                log.inf("Epoch {:3d}: train_loss={:.6f}, val_loss={:.6f}, lr={:.2e}".format(
                    epoch, epochLoss, valLoss, optimizer.param_groups[0]['lr']))

            if valLoss < bestValLoss:
                bestValLoss = valLoss
                bestState = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}
                patienceCounter = 0
            else:
                patienceCounter += 1
                if patienceCounter >= self.patience:
                    log.inf("Early stopping at epoch {}".format(epoch))
                    break

        self.model.load_state_dict(bestState)
        self.model.eval()
        log.inf("Done fitting: best val_loss={:.6f}, input_dim={}".format(bestValLoss, inputDim))

    def predict(self, xdf):
        X = self.scaler.transform(xdf.to_numpy().astype(np.float32))
        Xt = torch.tensor(X, dtype=torch.float32)
        preds = []
        with torch.no_grad():
            for i in range(0, len(Xt), self.batchSize):
                Xb = Xt[i: i + self.batchSize].to(device)
                preds.append(self.model(Xb).cpu().numpy())
        return np.concatenate(preds) / 100.0
