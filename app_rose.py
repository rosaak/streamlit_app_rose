import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import typing
import math
import pandas as pd

st.set_page_config(page_title='Rose Mathematics', layout="wide", initial_sidebar_state="auto", menu_items=None)

def get_xy(r: int, a: float): 
    x = r * np.cos(a)
    y = r * np.sin(a)
    return x,y


def calculate_rose(n :int, d: int, width: int, height: int, point_size):
    res = []
    k = n/d
    for i in np.arange(0, d*2*np.pi,  0.002):
        r = np.cos(k * i)
        _ = get_xy(r=r, a=i)
        res.append([r, i, _[0], _[1]])
    return pd.DataFrame(res, columns=["r", "a", "x", "y"])


def calculate02(n :int, d: int, width: int, height: int, point_size):
    def is_even(i):
        return i % 2 == 0
    res = []
    k = n/d
    st.write(k)
    if is_even(k):
        k=2*k
    for i in np.arange(0, d*2*np.pi,  0.001):
        r = np.cos(k * i)
        _ = get_xy(r=r, a=i)
        res.append([r, i, _[0], _[1]])
    return pd.DataFrame(res, columns=["r", "a", "x", "y"])


def calculate_limacon_trisectrix(n :int, d: int, width: int, height: int, point_size):
    res = []
    k = n/d
    for i in np.arange(0, d*2*np.pi,  0.002):
        r = i * (1 + (2* np.cos(i)))
        _ = get_xy(r=r, a=i)
        res.append([r, i, _[0], _[1]])
    return pd.DataFrame(res, columns=["r", "a", "x", "y"])

    
def plot2d(df, color: list, bgcolor: str):
    fig = px.scatter(df, 
                     x="x", 
                     y="y", 
                     width=width, 
                     height=height,
                     color_discrete_sequence=color
                     #color_continuous_scale=px.colors.sequential.Viridis #px.colors.qualitative.Antique
                    );
    fig.update_layout({
    'plot_bgcolor': bgcolor, # 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': bgcolor, #'rgba(0, 0, 0, 0)',
    'yaxis_visible': False, 
    'yaxis_showticklabels' :False,
    'xaxis_visible': False, 
    'xaxis_showticklabels' :False
    });
    fig.update_traces(marker=dict(size=point_size, line=dict(width=0, color='DarkSlateGrey')),
                      selector=dict(mode='markers'),
                      hovertemplate=None,
                      hoverinfo='skip'
                     )
    st.plotly_chart(fig, config={ 'modeBarButtonsToRemove': ['zoom', 'pan', 'Autoscale'] })
    
def plot3d(df, color: list, bgcolor:str):
    layout = go.Layout(
        plot_bgcolor="#FFF",  # Sets background color to white
        xaxis=dict(
            title="x",
            linecolor="#BCCCDC",  # Sets color of X-axis line
            showgrid=False  # Removes X-axis grid lines
        ),
        yaxis=dict(
            title="y",  
            linecolor="#BCCCDC",  # Sets color of Y-axis line
            showgrid=False,  # Removes Y-axis grid lines    
        )
    )
    
    fig = px.scatter_3d(df, 
                     x="x", 
                     y="y",
                     z="a",
                     # layout=layout,
                     width=width, 
                     height=height,
                     opacity=0.1,
                     color_discrete_sequence=color
                     #color_continuous_scale=px.colors.sequential.Viridis #px.colors.qualitative.Antique
                    );
    fig.update_layout({
    'plot_bgcolor': bgcolor, # 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': bgcolor, # 'rgba(0, 0, 0, 0)',
    'yaxis_visible': False, 
    'yaxis_showticklabels' :False,
    'xaxis_visible': False, 
    'xaxis_showticklabels':False,
    'template':'none' #'simple_white'
    });
    fig.update_traces(marker=dict(size=point_size, line=dict(width=0, color='DarkSlateGrey')),
                      selector=dict(mode='markers'),
                      hovertemplate=None,
                      hoverinfo='skip'
                     );
    
    # fig.update_layout(xaxis=dict(
    #     linecolor="#BCCCDC",  # Sets color of X-axis line
    #     showgrid=False  # Removes X-axis grid lines
    # ),
    # yaxis=dict(
    #     linecolor="#BCCCDC",  # Sets color of Y-axis line
    #     showgrid=False,  # Removes Y-axis grid lines    
    # ));
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    # fig.update_zaxis(showgrid=False)
    st.plotly_chart(fig, config={ 'modeBarButtonsToRemove': ['zoom', 'pan', 'Autoscale'] })




st.title("[Rose Mathematics](https://en.wikipedia.org/wiki/Rose_%28mathematics%29)")
st.caption("𝑟 = 𝑎 𝑐𝑜𝑠(𝑘𝜃)")
st.markdown('---')
col1, col2 = st.columns([1,6])
with col1:
    select_alg = st.radio("select algorithm", ("rose", "limacon trisectrix"))
    option_view = st.radio("plot as", ("2d", "3d"))
    st.markdown('---')
    nu = st.slider('n',1,100,3)
    de = st.slider('d',1,100,26)
    width = st.number_input('width', 100, 1000, 1000)
    height = st.number_input('height', 100, 1000, 1000)
    point_size = st.slider('point size',1.0,5.0,1.0, 0.01)
    # color = [st.selectbox('color', ["black", "white","red", "green", "blue", "goldenrod", "magenta"])]
    color = [st.color_picker('color picker', '#000000')]
    bgcolor = st.color_picker('bgcolor picker', '#FFFFFF')
    
with col2:
    
    #_df = calculate_limacon_trisectrix(nu, de, width, height, point_size)
    # plot3d(_df, color)
    if select_alg == 'rose' and option_view == '2d':
        _df = calculate_rose(nu, de, width, height, point_size)
        plot2d(_df, color, bgcolor)
    elif select_alg == 'rose' and option_view == '3d':
        _df = calculate_rose(nu, de, width, height, point_size)
        plot3d(_df, color, bgcolor)
    elif select_alg == 'limacon trisectrix' and option_view == '2d':
        _df = calculate_limacon_trisectrix(nu, de, width, height, point_size)
        plot2d(_df, color, bgcolor)
    elif select_alg == 'limacon trisectrix' and option_view == '3d':
        _df = calculate_limacon_trisectrix(nu, de, width, height, point_size)
        plot3d(_df, color, bgcolor)

st.markdown('---')

_="""
# TODO
- for each algorithm
 - use its own parameters
- how to remove the grids from plotly

"""