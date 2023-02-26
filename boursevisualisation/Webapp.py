import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.graph_objects as go

import GetVisual as gv

# Page setting
st.set_page_config(layout="wide")
st.title('Visualisation de votre portefeuille boursier')
st.subheader('Réalisé par Léandre Tuesta')
st.markdown('--------------', unsafe_allow_html=False)

co1, co2 =  st.columns(2)

with co1:
    st.metric(label="Date", value=str(gv.getFinalHist().iloc[-1]['Date'])[0:10])
with co2:
    st.metric(label="Evaluation", value=str(round(gv.getFinalHist().iloc[-1]['Open'], 2)) + "€", delta=str(round(gv.getFinalHist().iloc[-1]['Open']-gv.getInvest(), 2)) + "€")


df = st.table(pd.read_csv('Actions.csv', sep =';'))

st.write("Ajouter une nouvelle action")

col1, col2, col3, col4 = st.columns(4)

with col1:
   name = st.text_input(
        "Name",
        "name",
        key="name",
    )

with col2:
   symbole = st.text_input(
        "Symbole",
        "symbole",
        key="symbole",
    )

with col3:
   achat = st.text_input(
        "Prix d'achat",
        "1",
        key="achat",
    )

with col4:
   quantity = st.text_input(
        "Quantity",
        "1",
        key="quantity",
    )

## addition d'une action
if st.button('Add', key='add'):
    actions = pd.read_csv('Actions.csv', sep =';')
    actions=actions.append({'name' : name , 'symbole' : symbole, 'achat' : achat, 'quantity' : quantity} , ignore_index=True)
    actions.to_csv('Actions.csv', sep =';', index=False)

option = st.selectbox(
    'How would you like to be contacted?',
    pd.read_csv('Actions.csv', sep =';')['name'])

if st.button('Delete', key='delete'):
    actions = pd.read_csv('Actions.csv', sep =';')
    actions.drop(actions.index[actions[actions['name']==option].index.tolist()], inplace=True)
    actions.to_csv('Actions.csv', sep =';', index=False)

st.markdown('--------------', unsafe_allow_html=False)

"""
st.line_chart(gv.getFinalHist()['Close'],use_container_width=True)


fig, ax = plt.subplots()
plt.plot(gv.getFinalHist()['Close'])
st.pyplot(fig)

print(gv.getFinalHist().columns)

"""



data = gv.getFinalHist()

fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="symbol")])

fig.update_xaxes(type='category')
fig.update_layout(height=800)

st.plotly_chart(fig, use_container_width=True)

"""
non mise à jours du tableai actions 
faire la matplotlib ici 
graphe camembert répartittion 

"""

st.table(gv.getFinalHist())