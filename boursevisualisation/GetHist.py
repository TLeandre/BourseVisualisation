import yfinance as yf 
import pandas as pd 

def getHistorical(actions, inter):
    df = []
    for i in range(len(actions)):
        df.append(yf.download(actions['symbole'][i], start=actions['date'][i], end=None,  interval = inter))
        df[i].set_axis([ 'Open'+str(i), 'High'+str(i),'Low'+str(i),'Close'+str(i),'Adj Close'+str(i),'Volume'+str(i)], axis='columns', inplace=True)
    return df

def fusion(df, actions):
    
    ind = 0
    maxi = -1
    for i in range(len(actions)):
        if len(df[i]) > maxi:
            ind = i
    
    liste = list(range(len(actions)))
    del liste[ind]
    frame = df[ind]
    
    for i in liste:
        frame = pd.concat([frame, df[i]], axis=1)
        frame = frame.fillna(method="ffill")
        frame = frame.fillna(0)
    
    return frame

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

def Hist(inter):
    actions = pd.read_csv('Actions.csv', sep =';')  

    result = resultHist(fusion(getHistorical(actions, inter), actions), actions)

    result['Date'] = result.index
    
    return result


def getInvest():
    actions = pd.read_csv('Actions.csv', sep =';')

    sum = 0
    for i in range(len(actions)):
        sum += actions['quantity'][i] * actions['achat'][i]
    
    return sum
