from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt
import time
import pytz

IST=pytz.timezone("Asia/Kolkata")
def getHistroyData(client_id, access_token, stock_symbol, **kwargs):
    try:
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
    except Exception as e:
        print(e)
        return
    start_date = kwargs.get("start_date")
    end_date = kwargs.get("end_date")
    last_days = kwargs.get("last_days")
    timeframe = kwargs.get("timeframe", "15")
    

    if end_date is None:
        end_date=dt.datetime.now(IST)
    else:
        end_date=dt.datetime.fromisoformat(end_date).astimezone(IST)
    if start_date is None and last_days is None :
        last_days=60
        start_date=end_date-dt.timedelta(last_days)
    elif start_date is not None :
        start_date=dt.datetime.fromisoformat(start_date).astimezone(IST)
        last_days=(end_date-start_date).days
    
    stock_data=[]
    start_date_curr=start_date
    while start_date_curr<=end_date:
        end_date_curr=start_date_curr+dt.timedelta(60)
        print(start_date_curr.strftime("%Y-%m-%d")," : ",end_date_curr.strftime("%Y-%m-%d"))
        data = {
        "symbol": stock_symbol,
        "resolution": timeframe,
        "date_format": "1",
        "range_from": start_date_curr.strftime("%Y-%m-%d"),
        "range_to": end_date_curr.strftime("%Y-%m-%d"),
        "cont_flag": "1",
        }
        
        curr_stock_data=fyers.history(data=data)
        while(curr_stock_data['s']=="error"):
            curr_stock_data=fyers.history(data=data)
            time.sleep(5)
        stock_data.extend(curr_stock_data["candles"])
        start_date_curr=end_date_curr+dt.timedelta(1)
    stock_dataframe=pd.DataFrame(stock_data,columns=["date","open","high","low","close","volume"])
    del stock_data
    stock_dataframe["date"]=pd.to_datetime(stock_dataframe["date"],unit='s',utc=True).dt.tz_convert(IST)
    # stock_dataframe['date']=stock_dataframe.date.dt.tz_localize(pytz.utc).dt.tz_convert(IST)
    stock_dataframe.set_index('date',inplace=True)
    if kwargs.get("to_csv") is True :
        csv_path=kwargs.get("csv_path")
        if csv_path is None:
            stock_dataframe.to_csv(f"""{stock_symbol}_{end_date.strftime("%Y_%m_%d")}_{start_date.strftime("%Y-%m-%d")}.csv""",index=True)
        else:
            stock_dataframe.to_csv(csv_path,index=True)
    else:
        return stock_dataframe

if __name__=="__main__":
    access_token="""asfhkfnfjk ----ajdbabfohidbfa"""
    client_id="abcdefg-123"
    data=getHistroyData(client_id=client_id,access_token=access_token,stock_symbol="NSE:SBIN-EQ",start_date="2024-01-01",end_date="2024-10-01",to_csv=True,csv_path="./test.csv")

    
    
    
    
    
    
        

    
