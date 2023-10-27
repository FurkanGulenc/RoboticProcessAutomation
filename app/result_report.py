import pandas as pd
import os


def mapping():
    file_path = os.path.join(".", "app", "constant_data", "Mapping.xlsx")

    df = pd.read_excel(file_path)

    mapping_dict = df.set_index('Account Description')['Logo Kod'].to_dict()

    return mapping_dict


    
def process_excel_to_df(save_path_excel):

    
    df = pd.read_excel(save_path_excel)

    mapping_dict = mapping()

    selected_columns= ['AccountDescription','NativeAmount']
    df = df[selected_columns]

    df['Hesap Kodu'] = df['AccountDescription'].map(mapping_dict)

    df["NativeAmount"] = df["NativeAmount"].astype(str)

    return df

def process_excel_for_logo_bot(save_path_excel):

    df = pd.read_excel(save_path_excel)

    selected_columns = ["AccountDescription", "NativeAmount"]

    df = df[selected_columns]
    
    mapping_dict = mapping()

    df['Hesap Kodu'] = df['AccountDescription'].map(mapping_dict)

    df["NativeAmount"] = df["NativeAmount"].astype(str)

    df = df.drop("AccountDescription", axis=1)

    return df


    
def results(df):
    results = []

    for i in range(len(df)):
        sonuc = f'{df["AccountDescription"][i]} dan elde edilen {df["NativeAmount"][i]}₺ gelir, {df["Hesap Kodu"][i]} kodlu hesaba aktarılmalıdır. ' 
        results.append(sonuc)
 
    return "\\n".join(results)


