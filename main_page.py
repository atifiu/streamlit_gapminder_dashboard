import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
#import cv2
#from  PIL import ImageChops
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.express as px
import io
from common import set_page_container_style
import numpy as np
from raceplotly.plots import barplot
import os
print(os.getcwd())



def fn_year_series(df, type, name):
    if type == 'countrylist':
        if 'All' in name:
            return df['year'].unique()
        else:
            return df.query("country == @name[0]")['year'].unique()
    elif type == 'country':
            return df.query("country == @name")['year'].unique()
    elif type == 'continent':
        return df.query("continent == @name")['year'].unique()

def fn_summary_df(df):
    df_country = df.groupby(['year', 'continent']).agg({'pop':'sum', 'gdpPercap':'sum'}).reset_index()
    df_world = df.groupby('year').agg({'pop':'sum', 'gdpPercap':'sum'}).reset_index()
    df_world['continent'] = 'World'
    df_summary = pd.concat([df_country, df_world], sort = True, ignore_index = True)
    return df_summary

st.set_page_config(page_title="GapMinder data using Streamlit", page_icon=":rocket:", layout="wide")


# sysmenu = '''
# <style>
# #MainMenu {visibility:hidden;}
# footer {visibility:hidden;}
# '''
#st.markdown(sysmenu,unsafe_allow_html=True)

# Remove whitespace from the top of the page and sidebar
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



#Add a logo (optional) in the sidebar
#logo = Image.open(r'E:\python\dataVisualizations\streamlit_customizedmemu_app\images\Insights_Bees_logo.png')
logo = Image.open(r"images/Insights_Bees_logo.png")
profile = Image.open(r"images/Insights_Bees_logo.png")

with st.sidebar:
    choose = option_menu("App Gallery", [ "GapMinder Data"],
                         icons=[ 'bar-chart-fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )


logo = Image.open(r'E:\python\dataVisualizations\streamlit_customizedmemu_app\images\Insights_Bees_logo.png')
profile = Image.open(r'E:\python\dataVisualizations\streamlit_customizedmemu_app\images\Insights_Bees_logo.png')

if choose == "GapMinder Data":
    
    
    df = pd.DataFrame(px.data.gapminder())
    df_subset = df.drop(columns=['iso_alpha', 'iso_num'])
    #st.header("National Statistics")
    page = st.sidebar.selectbox('Select page',
    ['World GDP vs POP', 'Country data','Continent data'])
    if page == 'World GDP vs POP':
        st.header("World Population vs GDP")
        df_summary = fn_summary_df(df)
        total_pop, year = df_summary[(df_summary['year'] == df_summary['year'].max()) & (df_summary['continent'] == 'World')].iloc[0,[2,3]]
        max_pop_country, max_pop = df.sort_values(by = ['year', 'pop'], ascending = [False, False]).nlargest(1, 'pop').iloc[0,[0,4]]
        min_pop_country, min_pop = df.sort_values(by = ['year', 'pop'], ascending = [False, True]).nsmallest(1, 'pop').iloc[0,[0,4]]
        max_gdp_country, max_gdp = df.sort_values(by = ['year', 'gdpPercap'], ascending = [False, False]).nlargest(1, 'gdpPercap').iloc[0,[0,5]]
        min_gdp_country, min_gdp = df.sort_values(by = ['year', 'gdpPercap'], ascending = [False, True]).nsmallest(1, 'gdpPercap').iloc[0,[0,5]]
        #st.dataframe(df_summary)
        # create three columns
        metric1, metric2, metric3, metric4, metric5 = st.columns(5)

        # fill in those three columns with respective metrics or KPIs
        metric1.metric(
            label="World Population in Billions ",
            value=round((total_pop/1000000000), 2) 
            #delta=round(avg_age) - 10,
        )

        metric2.metric(
            label=f"Highest Pop. {max_pop_country}",
            value=round((max_pop/1000000000), 2) 
            #delta=round(avg_age) - 10,
        )

        metric3.metric(
            label=f"Lowest Pop. {min_pop_country[:10]} (In Millions)",
            value=round((min_pop/1000000), 2) 
            #delta=round(avg_age) - 10,
        )

        metric4.metric(
            label=f"Highest GDP {max_gdp_country} ",
            value=round(max_gdp) 
            #delta=round(avg_age) - 10,
        )

        metric5.metric(
            label=f"Lowest GDP {min_gdp_country} ",
            value=round(min_gdp) 
            #delta=round(avg_age) - 10,
        )

        

        
        col1, col2 = st.columns(2, gap='large')
        raceplot_country = barplot(df,  item_column='country', value_column='pop', time_column='year',top_entries=10
                            )
        fig=raceplot_country.plot(item_label = 'Country', value_label = 'Population in Billions', frame_duration = 'Year',  
                            orientation='horizontal')
        fig.update_layout(
        title='Population by Country',
        autosize=False,
        width=650,
        height=550
        #paper_bgcolor="lightgray",
        )
        col1.plotly_chart(fig, use_container_width=False)

        raceplot = barplot(df_summary,  item_column='continent', value_column='pop', time_column='year',top_entries=10
                            , item_color = {'World': 'rgb(0, 0, 255)', 'Asia': 'rgb(163, 208, 255)', 'Africa': 'rgb(236, 208, 255)',
                                    'Americas': 'rgb(236, 101, 229)', 'Europe': 'rgb(159, 226, 229)'})
        fig=raceplot.plot(item_label = 'Continent', value_label = 'Population in Billions', frame_duration = 'Year',  
                            orientation='horizontal')
        fig.update_layout(
        title='Population by Continent',
        autosize=False,
        width=650,
        height=550
        #paper_bgcolor="lightgray",
        )
        col2.plotly_chart(fig, use_container_width=False)

        
    elif page == 'Country data':
        type_radio = st.sidebar.radio("Select type of chart/data to display", ("DataTable", "LinePlots", "BubblePlots"))
        if type_radio == "LinePlots":
            st.header("Line Plots")
            ## Countries
            clist = df['country'].unique()
            country = st.selectbox("Select a country:",clist)
            year_series = fn_year_series(df, 'country',country)
            #year_series = df.query("country == @country")['year']
            start_year, end_year = st.sidebar.select_slider("Select start and end year", 
                                                    options = year_series,
                                                    value = (year_series.tolist()[0], year_series.tolist()[-1])
                                                    )
            #with st.container():
            #    col1, = st.columns(1)
            col1, col2 = st.columns(2)
            fig = px.line(df[(df['country'] == country) & (df['year'].between(start_year, end_year))], 
                    x = "year", y = "gdpPercap",title = "GDP per Capita")
            col1.plotly_chart(fig,use_container_width = True)
            #with st.container():
            #    col1, = st.columns(1)
            fig = px.line(df[(df['country'] == country) & (df['year'].between(start_year, end_year))], 
                    x = "year", y = "pop",title = "Population Growth")
            
            col2.plotly_chart(fig,use_container_width = True)
        elif type_radio == "DataTable":
            ##Grid config
            st.header("Data Table")
            
            gb = GridOptionsBuilder.from_dataframe(df_subset)
            gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
            gb.configure_side_bar() #Add a sidebar
            gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
            gridOptions = gb.build()
            grid_response = AgGrid(
                df_subset,
                gridOptions=gridOptions,
                data_return_mode='AS_INPUT', 
                update_mode='MODEL_CHANGED', 
                fit_columns_on_grid_load=False,
                theme='alpine', #Add theme color to the table
                enable_enterprise_modules=True,
                height=700, 
                width='50%',
                reload_data=False
            )

            data = grid_response['data']
            selected = grid_response['selected_rows'] 
            df_selected = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
        elif type_radio == "BubblePlots":
            st.header("Bubble Plot")
            clist = df['country'].unique()
            clist = np.insert(clist,0, 'All')
            country = st.multiselect("Select a country:",clist, default = 'All')
            
            if 'All' in country:
                col1, = st.columns(1)
                fig = px.scatter(data_frame = df,x = 'gdpPercap', y = 'lifeExp', color = 'continent',
                                animation_frame="year", animation_group="country" ,
                                size = 'pop', hover_name = 'country',  log_x=True, size_max=80, height=600, range_x=[100,100000], range_y=[25,90])
            
                st.plotly_chart(fig,use_container_width = True)
            else:
                col1, = st.columns(1)
                fig = px.scatter(data_frame = df[df['country'].isin(country)],x = 'gdpPercap', y = 'lifeExp', color = 'continent',
                                animation_frame="year", animation_group="country" ,
                                size = 'pop', hover_name = 'country',  log_x=True, size_max=80, height=600, range_x=[100,100000], range_y=[25,90])
            
                st.plotly_chart(fig,use_container_width = True)
            #with st.container():
           
            
    else:
        ## Continents
        st.header("Continent wise Statistics")
        contlist = df['continent'].unique()
        type_radio = st.sidebar.radio("Select type of chart/data to display", (["LinePlots"]))
        if type_radio == "LinePlots":
            
            continent = st.selectbox("Select a continent:",contlist)
            year_series = fn_year_series(df, 'continent',continent)
            
            start_year, end_year = st.sidebar.select_slider("Select start and end year", 
                                                        options = year_series,
                                                        value = (year_series.tolist()[0], year_series.tolist()[-1])
                                                        )
            col1,col2 = st.columns(2)
            fig = px.line(df[(df['continent'] == continent) & (df['year'].between(start_year, end_year))], 
                x = "year", y = "gdpPercap",
                title = "GDP per Capita",color = 'country')
            
            col1.plotly_chart(fig, use_container_width = True)
            fig = px.line(df[(df['continent'] == continent) & (df['year'].between(start_year, end_year))], 
                x = "year", y = "pop",
                title = "Population",color = 'country')
            
            col2.plotly_chart(fig, use_container_width = True)


