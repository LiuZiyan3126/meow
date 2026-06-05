import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("predictions.csv")

plt.scatter(df["forecast"], df["fret12"], s=0.1, alpha=0.3)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.plot([-0.01, 0.01], [-0.01, 0.01], "r--")
plt.savefig("scatter.png", dpi=150)

print(df[["forecast", "fret12"]].corr())
