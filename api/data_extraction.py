import tabula as tab
import pandas as pd


# For Hutch 381 pdf
def data_pipeline(pdf):
    df = pd.concat(pdf)
    dropped = df.drop(columns=['SEQ', 'Cell Id', 'Lac', 'Cell Name'])
    dropped['imsi'] = 0
    dropped.columns = ['caller', 'receiver', 'call_type',
                       'date_time', 'duration', 'imei', 'imsi']

    # one hot encoding call_type
    converted = pd.get_dummies(dropped['call_type'])
    combined = pd.concat((converted, dropped), axis=1)
    combined = combined.drop(["call_type"], axis=1)
    result = combined.rename(columns={"SMS-Incoming": "call_type"})
    return (result)


# For Dialog 398 pdf
def data_pipeline2(pdf):
    df = pd.concat(pdf)
    dropped = df.drop(columns=['No', 'Cell ID', 'Base station'])
    dropped['imsi'] = 0
    dropped.columns = ['imei', 'caller', 'receiver',
                       'date_time', 'call_type', 'duration', 'imsi']

    # one hot encoding call_type
    converted = pd.get_dummies(dropped['call_type'])
    combined = pd.concat((converted, dropped), axis=1)
    combined = combined.drop(["call_type", "ORIGIN"], axis=1)
    result = combined.rename(columns={"TERMI": "call_type"})
    return(result)


# For Airtel 416 pdf
def data_pipeline3(pdf):
    df = pd.concat(pdf)
    dropped = df.drop(columns=['Cell1', 'Cell2', 'Type SMSC'])
    dropped["date_time"] = dropped[["Date", "Time"]].apply(" ".join, axis=1)
    merged = dropped.drop(columns=['Date', 'Time'])
    merged.columns = ['caller', 'receiver', 'duration',
                      'call_type', 'imei', 'imsi', 'date_time']
    merged = merged[merged["call_type"].str.contains("SMS") == False]
    merged['date_time'] = pd.to_datetime(
        merged['date_time']).dt.strftime('%m/%d/%Y %H:%M:%S')

    # one hot encoding call_type
    converted = pd.get_dummies(merged['call_type'])
    combined = pd.concat((converted, merged), axis=1)
    combined = combined.drop(["call_type"], axis=1)
    result = combined.rename(columns={"Incoming Call-MTC": "call_type"})
    return(result)


# For Mobitel 435 pdf
def data_pipeline4(pdf):
    df = pd.concat(pdf)
    dropped = df.drop(columns=['MSISDN', 'Cell ID', 'Cell Name'])
    dropped["date_time"] = dropped[["Date", "Time"]].apply(" ".join, axis=1)
    merged = dropped.drop(columns=['Date', 'Time'])
    merged.columns = ['caller', 'receiver', 'call_type',
                      'duration', 'imei', 'imsi', 'date_time']
    converted = pd.get_dummies(merged['call_type'])
    combined = pd.concat((converted, merged), axis=1)
    combined = combined.drop(["call_type", "Incoming"], axis=1)
    result = combined.rename(columns={"Outgoing": "call_type"})
    return(result)


def date_convert(date):
    dateSplit = date.split(" ")
    month = dateSplit[0][2: 4]
    date = dateSplit[0][0: 2]
    year = dateSplit[0][4:]

    hour = dateSplit[1][0: 2]
    minutes = dateSplit[1][2: 4]
    seconds = dateSplit[1][4:]

    date_format = month+"/"+date+"/"+year+" "+hour+":"+minutes+":"+seconds
    return date_format
