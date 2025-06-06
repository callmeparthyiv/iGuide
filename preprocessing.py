import pandas as pd

class DataPrep:
    fileName = []
    
    def __init__(self, files):
        self.fileName = files
    
    def data_extract(self):
        keyword = "Watch"
        df = pd.read_csv(self.fileName[0])
        df1 = pd.read_csv(self.fileName[1])
        df2 = pd.read_csv(self.fileName[2])
        df = df[df['Device'].str.contains(keyword, case=False)]
        df1 = df1[df1['Device'].str.contains(keyword, case=False)]
        df2 = df2[df2['Device'].str.contains(keyword, case=False)]
        
        
        df = pd.concat([df,df1,df2], ignore_index=True)
        
        df.to_csv('Apple_Watch_data.csv', index=False)
        

d1 = DataPrep(['gsm_dataset_1.csv','gsm_dataset_2.csv', 'gsm_dataset_3.csv'])
d1.data_extract()


        
        