import streamlit as st 
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import time
from query import *

#page setting page icon will change in icon of page

st.set_page_config(page_title='Dashboard',page_icon='🤮',layout='wide') 


#st.markdown("<style> header {visibility: hidden;} </style>", unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


# creating header

st.subheader('⚙ Welcome To Insurance Analysis !')
st.markdown("##")

# getting data from query and print on web page
#st.dataframe(df)


# side bar logo
image_height = 200
st.sidebar.image("actiknow_image.png", caption= 'ActiKnow Consulting')
# filter data


# blow one is use fixed choose option
# options  = st.sidebar.multiselect("select Region", ["Central" ,
#                     "East", "Midwest","Northeast"] )

# for creating dynamic we use unique from df

Regions = st.sidebar.multiselect(
    "Select Region", 
    options = list(df["region"].unique()),
    default = df["region"].unique() 
    )

Location = st.sidebar.multiselect(
    "Select Location", 
    options  = list(df["location"].unique()), 
    default = df["location"].unique()
    )

State = st.sidebar.multiselect('"Select State',
                               options  = df["state"].unique(),    
                               default = df["state"].unique())
selected_df = df.query(
              "region == @Regions & location == @Location & state == @State"
    
        )

# for seeing the table after filter use this
#st.dataframe(selected_df)
# this is use for putting the horizantal line accros the screen
#st.markdown("---")
# function for number formating


def Format_number(num):
    if num >= 1000000:
        return f'{num/100000:.2f}M'
    elif num >=1000:
        return f'{num/ 1000:.2f}K'
    else:
        return num
    


def home():
    with st.expander("Click to see your table"):
        show_data = st.multiselect("Choose Column you wannt" ,selected_df.columns)
        st.write(selected_df[show_data])
    
    

    # kpi buildup
    Total_policy   = selected_df['policy'].count()
    Total_Investment =  Format_number(selected_df['investment'].sum())
    #Investment_mode  =  (int(selected_df['investment'].mode().iloc[0] if not selected_df.empty else 0))
    Average_Investment  = Format_number(selected_df['investment'].mean())
    Rating     = round(selected_df['rating'].mean(),2)
    SUM_RATING = round(selected_df['rating'].sum(),2)


#each column width define



    a,b,d,e = st.columns([5,5,5,5], gap ='large')



#  this the way to format the number 
#  st.metric("Amount $ :",f"{Total_Investment:,.0f}")  for doing inside
#  "{:,.0f}".format(int(selected_df['investment'].sum()))    for doing inside

    with a:
        st.info("Policy_Count", icon= '📍')
        st.metric("Count: " , Total_policy )


    with b: 
        st.info("Total_Investment", icon= '📍')
        st.metric("Amount $ :" , Total_Investment)
#  this for reducing the text sized inside the with
#    st.markdown(f"<h1 style='font-size:16px;'>{Total_Investment}</h1>", unsafe_allow_html=True)

    # with c:
    #     st.info("Most Frequent", icon= '📍' )
    #     st.metric('Amount $ :',Investment_mode )

    with d:
        st.info('Average_Investment', icon= '📍')
        st.metric('Amount $ :' , Average_Investment  )

    with e:
        st.info("Rating", icon = '📍')
        st.metric('Average_Rating :',Rating, help = f"Total Rating sum : {SUM_RATING}" )

    st.markdown("---")
    

def graph():
    g, h = st.columns(2)
    # data for bar chart
    investment_count = selected_df.groupby('businesstype')['investment'].count().reset_index(name="Number of investment").sort_values('Number of investment',ascending = True)
    #investment_count =investment_count.sort_values('Number of investment',ascending = False)
    # data for pie chart
    investment_sum = selected_df.groupby('region')["investment"].sum().reset_index(name ="Total Investment Region Wise")
    with g:
        st.info("Policy_Count By Business Type")
        fig = px.bar(investment_count,
                     x="Number of investment",
                     y = "businesstype",
                     title= "Policy_Count By Business Type",
                     color= "Number of investment" )
    
    with h:
        st.info("policy")
        fig_2 = px.pie(investment_sum,names='region',values="Total Investment Region Wise")

    
    


    k = st.columns(1)[0]
    with k:
        st.info("Region, State And Loaction Wise Investment Analysis", icon = "🌳")
        treemap_data = selected_df.groupby(["region","state","location"])["investment"].sum().reset_index(name = "Investment")
        fig_3 = px.treemap(treemap_data, path=(["region","state","location"]), values="Investment")
        fig_3.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    
    g.plotly_chart(fig, use_container_width = True)
    h.plotly_chart(fig_2,use_container_width = True)
    k.plotly_chart(fig_3,use_container_width=True)




def progressbar():
    
    
    target  = 350000000
    target_format = Format_number(target)
    current = selected_df["investment"].sum()
    percent = min(round((current/target)*100),100)
    
    # if percent < 30:
    #     color = "#C10505"  # Red color
    # elif 30 <= percent <= 60:
    #     color = "yellow"  # Yellow color
    # else:
    #     color = "#15FF0D"  # Green color

    # st.write(
    #     f"""
    #     <style>
    #         .stProgress > div > div   {
    #             background-color:  {color};
    #         }
    #     </style>
    #     """, unsafe_allow_html=True
    # )

    my_bar = st.progress(percent)

    
    
    
    if percent >= 100:
        st.subheader("👍 Well Done Target Achieved")
    else:
        st.write ("You have Achieved" , percent , "% of Target Value " , target_format, "$")
    
    
    
    for percent_complete in range(percent):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=f"Target = {target_format}")



progressbar()

home()
graph()


st.write("                                           This Analysis is done python script bases and reference")




# #hide theme
# hide_st_style ="""

# <style>


# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}

# <style>
# """












































