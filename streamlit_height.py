import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

st.set_page_config(
        page_title="Teens' Height - Greece",
)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv(r'/Users/charalamposp/Documents/YOLO_Margi/train_yolo_to_detect_custom_object/yolo_custom_detection/height_gr.csv')
df2=df.groupby(['Age group','Sex','Year']).mean()

df3=df2['Mean height'].reset_index()
dfb=df3[df3['Sex']=='Boys'].groupby(['Year','Age group']).mean().reset_index()
dfg=df3[df3['Sex']=='Girls'].groupby(['Year','Age group']).mean().reset_index()


cols=[element for element in range(1985, 2020)]
b=np.zeros((15,len(cols)))
g=np.zeros((15,len(cols)))
for i,y in enumerate(cols):
    b[:,i] = dfb['Mean height'][dfb['Year']==y]
    g[:,i] = dfg['Mean height'][dfg['Year'] == y]

cols_str=[str(element) for element in range(1985, 2020)]

dfboys=pd.DataFrame(b, columns = cols_str)
dfgirls=pd.DataFrame(g, columns = cols_str)

dfboys.index = range(5, 20)
dfboys.index.name = 'Age'

dfgirls.index = range(5, 20)
dfgirls.index.name = 'Age'

total_gender_num=len(df[df['Sex']=='Boys'])


## bar plot data
dfms=pd.DataFrame([])

Dm=df.groupby(['Year','Sex']).mean().reset_index()
Ds=df.groupby(['Year','Sex']).std().reset_index()
Dmean_boys=Dm[Dm['Sex']=='Boys']
Dstd_boys=Ds[Ds['Sex']=='Boys']

Dmean_girls=Dm[Dm['Sex']=='Girls']
Dstd_girls=Ds[Ds['Sex']=='Girls']

cols=[element for element in range(1985, 2020)]
bms=np.zeros((len(cols),2))
gms=np.zeros((len(cols),2))
for i,y in enumerate(cols):
    bms[i,0] = Dmean_boys['Mean height'][Dmean_boys['Year']==y]
    bms[i,1] = Dstd_boys['Mean height'][Dstd_boys['Year']==y]
    gms[i, 0] = Dmean_girls['Mean height'][Dmean_girls['Year'] == y]
    gms[i, 1] = Dstd_girls['Mean height'][Dstd_girls['Year'] == y]


dfboysms=pd.DataFrame(bms, index = cols_str,columns=['Mean','Std'])
dfgirlsms=pd.DataFrame(gms, index = cols_str,columns=['Mean','Std'])



##

# st.sidebar.write("# Select Data to Visualize")

with st.sidebar:
    st.markdown("<h1 style='text-align: left; color: grey;'>Select Data to Visualize</h1>",unsafe_allow_html=True)


    gender = st.radio("Select Gender",('Male', 'Female'))

    if gender == 'Male':
        df=dfboys
        genderstr='Boys'
        dfms=dfboysms

    else:
        df=dfgirls
        genderstr = 'Girls'
        dfms = dfgirlsms



    columns = st.multiselect("Select Years", df.columns)
    filter = st.radio("Choose by:", ("inclusion", "exclusion"))




    if filter == "exclusion":
        columns = [col for col in df.columns if col not in columns]

    perc = len(columns) * 15 * 100 / total_gender_num

    st.dataframe(df[columns])

    with st.spinner("Loading..."):
        time.sleep(0.1)
    st.success("Done!")


##
st.markdown("<h3 style='text-align: center; color: grey;'>Teens\' height in Greece (1985-2019)</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)


##
with col1:
    fig = px.line(df[columns],markers=True)
    fig.update_layout(yaxis_title='Mean Height')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


##

with col2:

    dfp = pd.DataFrame(np.round(np.array([perc,100-perc]),2))
    dfp.index=[genderstr+' Included',genderstr+' Not Included']
    dfp.columns=['Percentage']
    fig2 = px.pie(dfp,values='Percentage',names=dfp.index.tolist(),
    color=dfp.index.tolist(),
    color_discrete_map={dfp.index.tolist()[0]:'#800020',
                        dfp.index.tolist()[1]:'#f0d0d0'})
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)



#
# figbar = px.scatter(dfms.loc[columns], error_y="Std")
# figbar.update_yaxes(range=[50, 180], row=1, col=1)
#
# st.plotly_chart(figbar, theme="streamlit", use_container_width=True)
#

