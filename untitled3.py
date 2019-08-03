
import numpy as np
import pandas as pd
mg = pd.read_csv('C:/Users/yogi reddy/Desktop/pythonproject/dataset.csv')
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from datetime import datetime
mg.head(3)
mg.shape
mg.info()
mg['Region of Incident'].value_counts().plot.bar()
pd.pivot_table(mg,values='Total Dead and Missing',index='Reported Date',aggfunc=np.sum).sort_index().head()
date_s = mg.iloc[1,2]
date_s
date_test = datetime.strptime(date_s,'%B %d, %Y')
print(date_test)
mg['Reported Date dt']= mg['Reported Date'].apply(lambda x: datetime.strptime(x,'%B %d, %Y'))
pd.pivot_table(mg,values='Total Dead and Missing',index='Reported Date dt',aggfunc=np.sum).sort_index().plot()
pd.pivot_table(mg,values='Total Dead and Missing',index='Reported Year',aggfunc=np.sum).sort_index().plot(kind='bar')
pd.pivot_table(mg,values='Total Dead and Missing',index='Reported Year',aggfunc=np.sum).sort_index()
print('Maximum date is : {}'.format(mg['Reported Date dt'].max()))
print('Minimum date is : {}'.format(mg['Reported Date dt'].min()))

pd.pivot_table(mg,values=['Number of Males','Number of Females','Number of Children'],
               index='Reported Year',
               aggfunc={'Number of Males': np.sum,'Number of Females': np.sum,'Number of Children': np.sum}).plot(kind='bar')
mg['Total MFC']= mg['Number of Males']+mg['Number of Females']+mg['Number of Children']
mg[mg['Total MFC']==mg['Total Dead and Missing']].shape[0]
mg_reportMFC = mg[mg['Total MFC']==mg['Total Dead and Missing']]
datasets=[mg,mg_reportMFC]

for data in datasets:
    pd.pivot_table(data,values=['Number of Males','Number of Females','Number of Children'],
                   index='Reported Year',
                   aggfunc={'Number of Males': np.sum,'Number of Females': np.sum,'Number of Children': np.sum}).plot(kind='bar')
  


# In[22]:


pd.pivot_table(mg,values=['Number of Males','Number of Females','Number of Children'],
               index='Reported Year',
               aggfunc={'Number of Males': np.sum,'Number of Females': np.sum,'Number of Children': np.sum})

tidy =pd.pivot_table(mg_reportMFC,values=['Number of Males','Number of Females','Number of Children'],
               index='Reported Year',
               aggfunc={'Number of Males': np.sum,'Number of Females': np.sum,'Number of Children': np.sum})

tidy['year']=tidy.index
pd.melt(tidy,id_vars=['year'])
lat_lon = mg['Location Coordinates'].str.split(',',expand=True).rename(index=int, columns={0: "lat", 1: "lon"})
mg =pd.concat([mg,lat_lon],axis=1)
mg.head()
import folium
mg.info()

mg['lat'] = mg['lat'].astype(float)
mg['lon'] = mg['lon'].astype(float)



max_lat =mg['lat'].max()
max_lon =mg['lon'].max()
