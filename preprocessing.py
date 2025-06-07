import pandas as pd

class DataPrep:
    fileName = []
    
    def __init__(self, files):
        self.fileName = files
    
    #extracting iphone/ipad/watch data from all the three dataset for preprocessing
    def data_extract(self):
        
        #keyword can be changed to extract specific device
        keyword = "Watch"
        df = pd.read_csv(self.fileName[0])
        df1 = pd.read_csv(self.fileName[1])
        df2 = pd.read_csv(self.fileName[2])
        
        #taking the record that matches the keyword
        df = df[df['Device'].str.contains(keyword, case=False)]
        df1 = df1[df1['Device'].str.contains(keyword, case=False)]
        df2 = df2[df2['Device'].str.contains(keyword, case=False)]
        
        #concating all the three dataframes and making  a csv file
        df = pd.concat([df,df1,df2], ignore_index=True)
        df.to_csv('Apple_Watch_data.csv', index=False)
    
    
    def data_preprocessing(self):
        
        #preprocessing iphone data selecting only necessary columns nrow 38 for selecting only first 38 rows
        df = pd.read_csv(self.fileName[0], 
                         usecols=['Device', 'Image_url', 'Source_url', 'Network - Technology','Launch - Announced',
                                'Launch - Status','Body - Weight','Body - Build', 'Body - SIM', 'Body - ',
                                'Display - Type', 'Display - Size','Display - Protection', 'Platform - OS',
                                'Platform - Chipset','Platform - GPU','Memory - Internal', 'Main Camera - Single', 
                                'Main Camera - Features','Main Camera - Video', 'Selfie camera - Single',
                                'Selfie camera - Features', 'Selfie camera - Video','Sound - 3.5mm jack',
                                'Comms - WLAN','Comms - Bluetooth','Comms - NFC','Comms - USB', 
                                'Features - Sensors', 'Battery - Type','Misc - Colors','Main Camera - Triple',
                                'Main Camera - Dual'], 
                         nrows=38)
        

        #for generating a single column Main Camera 
        a = df['Main Camera - Single'].loc[df['Main Camera - Single'].notna()]
        b = df['Main Camera - Dual'].loc[df['Main Camera - Dual'].notna()]
        c = df['Main Camera - Triple'].loc[df['Main Camera - Triple'].notna()]
        df['Main Camera - Single'] = pd.concat([a,b,c],axis=0).sort_index()
        df.drop(columns=['Main Camera - Dual', 'Main Camera - Triple'], axis = 1, inplace=True)
        
        #renaming  all the columns
        df.rename(columns={"Main Camera - Single":"Main Camera"}, inplace=True)
        print(df.info())
        
        
        

# d1 = DataPrep(['gsm_dataset_1.csv','gsm_dataset_2.csv', 'gsm_dataset_3.csv'])
# d1.data_extract()

preprocessor = DataPrep(['iPhone_data.csv'])
preprocessor.data_preprocessing()        
        