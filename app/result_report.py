import pandas as pd
import pdfkit


def mapping():
    file_path = "./app/constant_data/Mapping.xlsx"

    df = pd.read_excel(file_path)

    mapping_dict = df.set_index('Account Description')['Logo Kod'].to_dict()

    return mapping_dict


    


"""mapping_dict = {
        "Mgd Dep Cash Other 4" : '120.051.0005',
        #"Mgd Dep Cash Other 5": '611.01.03',
        "AR Guest Ledger": '181.01.01.0001',
        "AR City Ledger": '1.200.510.001',
        "AR Credit Card MC Visa": '108.02.0001',
        "AR Credit Card AMEX": '108.02.0001',
        #"AR CCard JCB Discover Diners": '611.01.03',
        "Clearing Account 2" : '108.02.0001',
        "Cash Sales": '100.01.01.0002',
        #"HHonors Clearing Account": '611.01.03',
        "Deposits - Guest Advance": '340.01.01.A0001',
        "Sales Tax Payable Other 4": '391.01.01.0005',
        "Sales Tax Payable Other 5": '391.01.01.0004',
        "Sales Tax Payable Other 6": '391.01.01.0004',
        "Sales Tax Payable Other 13": '360.01.06.0001',
        "Best Available Rate Room Rev": '600.01.05.0001',
        "Consortia Room Revenue": '600.01.05.0001',
        "Corp Negotiated Room Revenue": '600.01.05.0001',
        "Local Negotiated Room Revenue": '600.01.05.0001',
        "Individual Tour Wholesale Room": '600.01.05.0001',
        "Corp Mktg Program Room Revenue": '600.01.05.0001',
        "Discounts Room Rev": '611.01.05.0001',
        "Company Meetings & Incentive": '600.01.05.0001',
        "Other Revenue": '600.01.05.0001',
        "Best Available Rate Occ Rooms": '600.01.05.0001',
        "Consortia Occ Rooms": '600.01.05.0001',
        "Corporate Negotiated Occ Rooms": '600.01.05.0001',
        "Local Negotiated Occ Rooms": '600.01.05.0001',
        "Indiv Tour Wholesale Occ Rooms": '600.01.05.0001',
        "Corp Mkt Revenue Occ Rooms": '600.01.05.0001',
        "Other Discounts Occ Rooms": '611.01.05.0001',
        "Co Meeting & Incentive Occ Rms": '600.01.05.0001',
        #"House Use Room Nights": '600.01.05.0001',
        "Out of Order Room Nights": '800.50.00.007',
        "Vacant Rooms": '800.50.00.005',
        "Number of Guests": '800.50.00.010',
        "Total Available Rooms": '800.50.00.001',
        "Total Occupied Rooms": '800.50.00.004',
        "Transient Arrivals": '800.50.00.012',
        "Departures": '800.50.00.008',
        "Breakfast Food Revenue": '600.01.05.0003',
        "Lunch Food Revenue": '600.01.05.0003',
        "Dinner Food Revenue": '611.01.03',
        "Food Allowance": '600.01.05.0003',
        "Other Beverage Revenue": '600.01.05.0011',
        "Sundry": '600.01.05.0011',
        "Lunch Food Revenue": '611.01.03',
        ##"Other Beverage Revenue": '611.01.03',
        "Lunch Food Revenue": '611.01.03',
        "Food Allowance": '611.01.03',
        "Beer Revenue": '600.01.05.0005',
        "Wine Revenue": '611.01.03',
        "Liquor Revenue": '611.01.03',
        ###"Other Beverage Revenue": '611.01.03',
        "Sundry": '611.01.03',
        "Breakfast Food Revenue": '611.01.03',
        "Lunch Food Revenue": '611.01.03',
        "Dinner Food Revenue": '611.01.03',
        "Beer Revenue": '611.01.03',
        "Wine Revenue": '611.01.03',
        "Liquor Revenue": '611.01.03',
        "Other Beverage Revenue": '611.01.03',
        "Beverage Allowance": '611.01.03',
        "Sundry": '611.01.03',
        "Breakfast Food Revenue": '611.01.03',
        "Lunch Food Revenue": '611.01.03',
        "Dinner Food Revenue": '611.01.03',
        "Food Allowance": '611.01.03',
        "Wine Revenue": '611.01.03',
        "Other Beverage Revenue": '611.01.03',
        "Sundry": '611.01.03',
        "Other Food Revenue": '611.01.03',
        "Beer Revenue": '600.01.05.0005',
        "Wine Revenue": '600.01.05.0005',
        "Liquor Revenue": '600.01.05.0005',
        #"Other Beverage Revenue": '611.01.03',
        "Lunch Food Revenue": '611.01.03',
        "Dinner Food Revenue": '611.01.03',
        "Wine Revenue": '611.01.03',
        "Liquor Revenue": '611.01.03',
        "Other Beverage Revenue": '611.01.03',
        "Guest Laundry": '600.01.05.0011',
        "Valet Parking": '600.01.05.0011',
        "Retail Sundries": '600.01.05.0011',
        "Other Revenue": '600.01.05.0011',
        "FX Gain Loss Other": '656.01.01.0008',
    }

"""
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


"""results = []

    for i in range(len(df_data)):
        sonuc = f'{df_data["AccountDescription"][i]} dan elde edilen {df_data["NativeAmount"][i]}₺ gelir, {df_data["Hesap Kodu"][i]} kodlu hesaba aktarılmalıdır.'
        results.append(sonuc)"""
    


"""def convert_pdf(save_path_excel):

    df = pd.read_excel(save_path_excel)

    html = df.to_html()

    pdf = pdfkit.from_string(html, "trialBalance.pdf")"""

