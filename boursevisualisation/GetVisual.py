import yfinance as yf 
import pandas as pd 

def getActionsHist(actions):
    df=[]

    for i in range(len(actions)):
        df.append(yf.Ticker(actions['symbole'][i]).history(period='1d', start='2022-9-1', end=None))
        df[i].drop(df[i].iloc[:, 4:8], axis=1, inplace=True)
        df[i].set_axis([ 'Open'+str(i), 'High'+str(i),'Low'+str(i),'Close'+str(i)], axis='columns', inplace=True)
    return df

def concatHist(df, actions):
    if len(actions) >= 2:
        concatdf = pd.concat([df[0], df[1]], axis=1)
    else:
        concatdf = df[0]

    for i in range(2,len(actions)):
        concatdf = pd.concat([concatdf, df[i]], axis=1)
    concatdf = concatdf.fillna(method='ffill')
    concatdf = concatdf.fillna(method='bfill')
    
    return concatdf

def resultHist(concatdf, actions):
    result = pd.DataFrame(columns=["Open","High","Low","Close"])

    result["Open"] = concatdf["Open0"]*actions['quantity'][0]
    result["High"] = concatdf["High0"]*actions['quantity'][0]
    result["Low"] = concatdf["Low0"]*actions['quantity'][0]
    result["Close"] = concatdf["Close0"]*actions['quantity'][0]


    for i in range(1,len(actions)):

        result["Open"] += concatdf["Open"+str(i)]*actions['quantity'][i]
        result["High"] += concatdf["High"+str(i)]*actions['quantity'][i]
        result["Low"] += concatdf["Low"+str(i)]*actions['quantity'][i]
        result["Close"] += concatdf["Close"+str(i)]*actions['quantity'][i]

    return result

def getFinalHist():
    actions = pd.read_csv('Actions.csv', sep =';')
    
    df = getActionsHist(actions)
    
    concatdf = concatHist(df, actions)
    
    finaldf = resultHist(concatdf, actions)

    finaldf['Date'] = finaldf.index
    
    return finaldf


def getInvest():
    actions = pd.read_csv('Actions.csv', sep =';')

    sum = 0
    for i in range(len(actions)):
        sum += actions['quantity'][i] * actions['achat'][i]
    
    return sum
