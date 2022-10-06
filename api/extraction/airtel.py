import tabula as tab
import pandas as pd

# For Airtel 416 pdf


def data_cleaning3(df):
    final = pd.DataFrame()

    if 'Unnamed: 0' in df.columns:
        dropped = withNull(df)
        dropped['CallType'].fillna('', inplace=True)
        dropped['Unnamed: 0'].fillna('', inplace=True)

        dropped["call_type"] = dropped[["CallType",
                                        "Unnamed: 0"]].apply(" ".join, axis=1)
        dropped = dropped.drop(
            columns=['CallType', 'Unnamed: 0'], axis=1, errors='ignore')

        final = final_data_cleaning3(dropped)

    else:
        final = withoutNull(df)

    return final


def withNull(dataframe):
    dropped = dataframe.drop(columns=['Cell1', 'Cell2', 'Type',
                                      'SMSC', 'RoamNW'], errors='ignore')
    dropped = dropped.dropna(subset=['CallingNO'])
    dropped["date_time"] = dropped[["Date", "Time"]].apply(" ".join, axis=1)
    merged = dropped.drop(columns=['Date', 'Time'])

    merged['date_time'] = pd.to_datetime(
        merged['date_time'], errors='coerce').dt.strftime('%m/%d/%Y %H:%M:%S')

    return merged


def withoutNull(dataframe):
    dropped = dataframe.drop(
        columns=['Cell1', 'Cell2', 'Type', 'SMSC', 'RoamNW'], errors='ignore')
    dropped = dropped.dropna()
    dropped["date_time"] = dropped[["Date", "Time"]].apply(" ".join, axis=1)
    merged = dropped.drop(columns=['Date', 'Time'])
    merged.columns = ['caller', 'receiver', 'duration',
                      'call_type', 'imei', 'imsi', 'date_time']

    merged['date_time'] = pd.to_datetime(
        merged['date_time'], errors='coerce').dt.strftime('%m/%d/%Y %H:%M:%S')

    if merged['call_type'].str.contains('Incoming Call', case=False).any():
        merged.loc[merged['call_type'].str.contains(
            'Incoming Call', case=False, na=False), 'call_type'] = 1

    if merged['call_type'].str.contains('Outgoing Call', case=False).any():
        merged.loc[merged['call_type'].str.contains(
            'Outgoing Call', case=False, na=False), 'call_type'] = 0

    if merged['call_type'].str.contains('Incoming SMS', case=False).any():
        merged.loc[merged['call_type'].str.contains(
            'Incoming SMS', case=False, na=False), 'call_type'] = 3

    if merged['call_type'].str.contains('Outgoing SMS', case=False).any():
        merged.loc[merged['call_type'].str.contains(
            'Outgoing SMS', case=False, na=False), 'call_type'] = 2

    return merged


def final_data_cleaning3(df):
    df.columns = ['caller', 'receiver', 'duration',
                  'imei', 'imsi', 'date_time', 'call_type']

    if df['call_type'].str.contains('Incoming Call', case=False).any():
        df.loc[df['call_type'].str.contains(
            'Incoming Call', case=False, na=False), 'call_type'] = 1

    if df['call_type'].str.contains('Outgoing Call', case=False).any():
        df.loc[df['call_type'].str.contains(
            'Outgoing Call', case=False, na=False), 'call_type'] = 0

    if df['call_type'].str.contains('Incoming SMS', case=False).any():
        df.loc[df['call_type'].str.contains(
            'Incoming SMS', case=False, na=False), 'call_type'] = 3

    if df['call_type'].str.contains('Outgoing SMS', case=False).any():
        df.loc[df['call_type'].str.contains(
            'Outgoing SMS', case=False, na=False), 'call_type'] = 2

    return df


# Final callable function(Should pass pdf path to this)
def airtel_pipeline(pdf_path):
    final = pd.DataFrame()
    result = pd.DataFrame()

    pdf = tab.read_pdf(pdf_path, pages="all")

    for index in range(0, len(pdf)+1):
        df = tab.read_pdf(pdf_path, pages=index)
        for frames in df:
            data = frames
            final = pd.concat([final, data], ignore_index=True)

    result = data_cleaning3(final)

    return result
