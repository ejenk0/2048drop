import json
from matplotlib import pyplot as plt
import datetime as dt

import pandas as pd

with open("performance_history.json", "r") as f:
    data = json.load(f)

recent = list(
    max(data.items(), key=lambda kv: dt.datetime.strptime(kv[0], "%y/%m/%d %H:%M.%S"))
)
recent[0] = dt.datetime.strptime(recent[0], "%y/%m/%d %H:%M.%S")
recent[1]["raw"] = {int(k): v for k, v in recent[1]["raw"].items()}

df = pd.DataFrame.from_dict(recent[1]["raw"], orient="index")
df.index = pd.to_datetime(df.index, unit="ms")
print(df)
df["aps"].plot()
plt.show()

# plt.plot(list(recent[1].keys()), [x["sps"] for x in recent[1].values()])
# plt.show()
