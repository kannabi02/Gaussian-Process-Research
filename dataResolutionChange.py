import pandas as pd
import numpy as np
import sys, os

def resolutionChange(PATH, outfile):
    df = pd.read_csv(PATH)
    colnames = []
    for col in df.columns:
        if not "Date" in col:
            if not "Time of day" in col:
                if not "Week" in col:
                    colnames.append(col)
    datescol = [col for col in df.columns if col not in colnames]
    dfnew = pd.DataFrame()

    if df.shape[0] % 4 != 0:
        df = pd.concat([df,pd.DataFrame(np.zeros([4-df.shape[0]%4,df.shape[1]]), columns=df.columns)], axis=0 )

    for col in colnames:
        tempdf = pd.DataFrame(df[col].values.reshape(-1,4))
        tempdf = tempdf.sum(axis=1)
        dfnew[col] = tempdf
    for col in datescol:
        tempdf = df[col].iloc[::4]
        tempdf.index = [i for i in range(len(tempdf))]
        dfnew = pd.concat([dfnew, tempdf],axis=1, ignore_index=True)
    dfnew.columns = colnames+datescol
    try:
        os.remove(outfile)
    except:
        pass

    dfnew.to_csv(outfile, index=False)

if __name__ == '__main__':
    resolutionChange(sys.argv[1], sys.argv[2])