##---- Import librairies 
import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import plotly.express as px

import GetHist as gh

##---- Commentaire 

##---- Page setting and Menu 

st.set_page_config(layout="wide")

c1, c2 = st.columns(2)

with c1:
    st.title('Visualisation de votre portefeuille boursier')
    st.subheader('Réalisé par Léandre Tuesta')
with c2:
    st.markdown('   ', unsafe_allow_html=False)
    st.markdown('   ', unsafe_allow_html=False)
    st.markdown('   ', unsafe_allow_html=False)
    selected = option_menu(
        menu_title=None,
        options=['Overview','Actions'],
        orientation="horizontal"
    )
st.markdown('--------------', unsafe_allow_html=False)

##---- Overview 

if selected == "Overview":
    co1, co2 =  st.columns(2)

    with co1:
        st.metric(label="Date de dernière mise à jour", value=str(gh.Hist('1d').iloc[-1]['Date'])[0:10])
    with co2:
        st.metric(label="Evaluation", value=str(round(gh.Hist('1d').iloc[-1]['Open'], 2)) + "€", delta=str(round(gh.Hist('1d').iloc[-1]['Open']-gh.getInvest(), 2)) + "€")
    
    st.markdown('--------------', unsafe_allow_html=False)

    ## Affichage des graphiques 
    collo1, collo2 =  st.columns(2)
    with collo1:
        frequency = st.selectbox(
            "Interval",
            ('1d','5d','1wk','1mo','3mo'))
    with collo2:
        option = st.selectbox(
            'Diagramme',
            ('Line chart', 'Japanese candlestick chart'))

    data = gh.Hist(frequency)

    if option == 'Line chart':

        fig = px.line(data, x="Date", y="Close", title='Line chart de votre portefeuille boursier')
    else:
        
        fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name="symbol")])

        fig.update_xaxes(type='category')
        fig.update_layout(height=800)
    
    st.plotly_chart(fig, use_container_width=True)


    ##graphique circulaire
    actions = pd.read_csv('Actions.csv', sep =';')
    actions['invest']=actions['achat']*actions['quantity']

    pie = px.pie(actions, values='invest', names='name', color_discrete_sequence=px.colors.sequential.RdBu, title="Répartition d'investissement sur le portefeuille")
    st.plotly_chart(pie, use_container_width=True)
    


##---- Actions 

if selected == "Actions":
    ## affichage de l'ensemble des actions présent dans le fichier csv 
    df = st.table(pd.read_csv('Actions.csv', sep =';'))

    ## Ajout et Suppression d'actions
    coAdd , coDel = st.columns(2)

    with coAdd:
        st.write("Ajouter une nouvelle action")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Name",
                "name",
                key="name",
            )
            achat = st.text_input(
                "Prix d'achat",
                "1",
                key="achat",
            )
            date = st.text_input(
                "Date d'achat",
                "AAAA-MM-JJ",
                key="date"
            )

        with col2:
            symbole = st.text_input(
                "Symbole",
                "symbole",
                key="symbole",
            )
            quantity = st.text_input(
                "Quantity",
                "1",
                key="quantity",
            )
            ## addition d'une action
            if st.button('Add', key='add'):
                actions = pd.read_csv('Actions.csv', sep =';')
                actions=actions.append({'name' : name , 'symbole' : symbole, 'achat' : achat, 'quantity' : quantity, 'date' : date} , ignore_index=True)
                actions.to_csv('Actions.csv', sep =';', index=False)
    with coDel:
        st.write("Supprimer une action")

        option = st.selectbox(
            "Selectionner l'action à supprimer",
            pd.read_csv('Actions.csv', sep =';')['name'])

        if st.button('Delete', key='delete'):
            actions = pd.read_csv('Actions.csv', sep =';')
            actions.drop(actions.index[actions[actions['name']==option].index.tolist()], inplace=True)
            actions.to_csv('Actions.csv', sep =';', index=False)

    st.markdown('--------------', unsafe_allow_html=False)

    ##---- Indicateur de chaque actions
    actions = pd.read_csv('Actions.csv', sep =';')
    coll1, coll2, coll3, coll4 = st.columns(4)
    for i in range(len(actions)):
        if (i % 4) == 0:
            with coll1:
                actualPrice = gh.getHistorical(actions, '1d')[i].iloc[-1]['Close'+str(i)]
                st.metric(
                    label=actions['symbole'][i], 
                    value=str(round(actualPrice, 2)),
                    delta=str(round(actualPrice - actions['achat'][i], 2)) + "€",
                )
        elif (i % 4) == 1:
            with coll2:
                actualPrice = gh.getHistorical(actions, '1d')[i].iloc[-1]['Close'+str(i)]
                st.metric(
                    label=actions['symbole'][i], 
                    value=str(round(actualPrice, 2)),
                    delta=str(round(actualPrice - actions['achat'][i], 2)) + "€",
                )
        elif (i % 4) == 2:
            with coll3:
                actualPrice = gh.getHistorical(actions, '1d')[i].iloc[-1]['Close'+str(i)]
                st.metric(
                    label=actions['symbole'][i], 
                    value=str(round(actualPrice, 2)),
                    delta=str(round(actualPrice - actions['achat'][i], 2)) + "€",
                )
        elif (i % 4) == 3:
            with coll4:
                actualPrice = gh.getHistorical(actions, '1d')[i].iloc[-1]['Close'+str(i)]
                st.metric(
                    label=actions['symbole'][i], 
                    value=str(round(actualPrice, 2)),
                    delta=str(round(actualPrice - actions['achat'][i], 2)) + "€",
                )
