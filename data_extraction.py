import tabula as tab
import pandas as pd

pdf = tab.read_pdf("../docs/1655367558381.pdf", pages='all')
pdf2 = tab.read_pdf("../docs/1655367558398.pdf", pages='all')
pdf3 = tab.read_pdf("../docs/1655367558416.pdf", pages='all')
pdf4 = tab.read_pdf("../docs/1655367558435.pdf", pages='all')


# For 381 pdf
def data_pipeline(pdf):
    df = pd.concat(pdf)
    name = df.head(5)
    dropped = name.drop(columns = ['SEQ','Cell Id','Lac','Cell Name'])
    dropped['imsi'] = 0
    dropped.columns = ['caller','receiver', 'call_type','date_time','duration','imei','imsi']
    
    # one hot encoding call_type
    converted = pd.get_dummies(dropped['call_type'])
    combined = pd.concat((converted,dropped), axis=1)
    combined = combined.drop(["call_type"] ,axis=1)
    result = combined.rename(columns={"SMS-Incoming": "call_type"})
    print(result)
    

# For 398 pdf
def data_pipeline2(pdf):
    df = pd.concat(pdf)
    dropped = df.drop(columns = ['No','Cell ID','Base station'])
    dropped['imsi'] = 0
    dropped.columns = ['imei','caller','receiver','date_time','call_type','duration','imsi']
    
    # one hot encoding call_type
    converted = pd.get_dummies(dropped['call_type'])
    combined = pd.concat((converted,dropped), axis=1)
    combined = combined.drop(["call_type","ORIGIN"] ,axis=1)
    result = combined.rename(columns={"TERMI": "call_type"})
    print(result)
    

# For 416 pdf
def data_pipeline3(pdf):
    df = pd.concat(pdf)
    name = df.head(30)
    dropped = name.drop(columns = ['Cell1','Cell2','Type SMSC'])
    dropped["date_time"] = dropped[["Date", "Time"]].apply(" ".join, axis=1)
    merged = dropped.drop(columns = ['Date', 'Time'])
    merged.columns = ['caller','receiver','duration','call_type','imei','imsi','date_time']
    merged = merged[merged["call_type"].str.contains("Incoming SMS-SMT|Outgoing SMS-SMS") == False]
    
    # one hot encoding call_type
    converted = pd.get_dummies(merged['call_type'])
    combined = pd.concat((converted,merged), axis=1)
    combined = combined.drop(["call_type"] ,axis=1)
    result = combined.rename(columns={"Incoming Call-MTC": "call_type"})
    print(result)


# For 435 pdf
def data_pipeline4(pdf):
    df = pd.concat(pdf)
    name = df.head(5)
    dropped = name.drop(columns = ['MSISDN','Cell ID','Cell Name'])
    dropped["date_time"] = dropped[["Date", "Time"]].apply(" ".join, axis=1)
    merged = dropped.drop(columns = ['Date', 'Time'])
    merged.columns = ['caller','receiver', 'call_type','duration','imei','imsi','date_time']
    converted = pd.get_dummies(merged['call_type'])
    combined = pd.concat((converted,merged), axis=1)
    combined = combined.drop(["call_type","Incoming"] ,axis=1)
    result = combined.rename(columns={"Outgoing": "call_type"})
    print(result)
    
    
# data_pipeline(pdf)
# print('-----------------------------------------')
# data_pipeline2(pdf2)
# print('-----------------------------------------')
data_pipeline3(pdf3)
# print('-----------------------------------------')
# data_pipeline4(pdf4)


       













# namelist = list(name["MSISDN"])

# allcount  = df['a Number'].value_counts()
# print('Full count of numbers ')
# print(allcount)

# count = (df['a Number'] == 710385942 ).sum()
# print(' ')
# print('specific number count is = ',count)