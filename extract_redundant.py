import pandas as pd
import numpy as np

df = pd.read_csv("USA-P1_Clusters.txt", sep="\t")
redSR = pd.DataFrame(df["Contig"].unique())
redSR.to_csv('SR_remove.txt', index = False, header = False)

