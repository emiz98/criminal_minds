import tabula as tab
import pandas as pd


def data_cleaning4(df):
    dropped = df.drop(columns=['MSISDN', 'Cell ID', 'Cell Name'])
    dropped["date_time"] = dropped[["Date", "Time"]].apply(" ".join, axis=1)
    merged = dropped.drop(columns=['Date', 'Time'])
    merged.columns = ['caller', 'receiver', 'call_type',
                      'duration', 'imei', 'imsi', 'date_time']
    merged['date_time'] = pd.to_datetime(
        merged['date_time'], errors='coerce').dt.strftime('%m/%d/%Y %H:%M:%S')

    if merged['call_type'].str.contains('Incoming', case=False).any():
        merged.loc[merged['call_type'].str.contains(
            'Incoming', case=False, na=False), 'call_type'] = 1

    if merged['call_type'].str.contains('Outgoing', case=False).any():
        merged.loc[merged['call_type'].str.contains(
            'Outgoing', case=False, na=False), 'call_type'] = 0

    return(merged)


def mobitel_pipeline(pdf):
    final = pd.DataFrame()

    for frames in pdf:
        data1 = frames.values

        columnVal = ['MSISDN', 'a Number', 'b Number', 'Event Type', 'Date',
                     'Time', 'Duration', 'Cell ID', 'Cell Name', 'IMEI', 'IMSI']

        data2 = pd.DataFrame(data=data1, columns=columnVal)
        final = pd.concat([final, data2], ignore_index=True)

    final = final.drop(index=0)
    result = data_cleaning4(final)

    result = result.drop(['Event Type'], axis=1, errors='ignore')

    result2 = result.drop(
        result.index[result['caller'] == 'a Number'], errors='ignore')

    return result2
