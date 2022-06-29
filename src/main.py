import streamlit as st

from boolean.boolean_model import *

from vectorial.cranfield.cranfield import *
from vectorial.cranfield.cranfield_manual_query import *
from vectorial.cisi.cisi import *
from vectorial.cisi.cisi_manual_query import *

from crawler.wiki_crawler import WikiCrawler

st.title('BIENVENIDO AL SISTEMA DE RECUPERACIÓN DE INFORMACIÓN') 
st.header('Escoja la opción deseada:')

option = 0

status = st.radio('', ('Procesar las consultas de la colección de datos', 
                        'Realizar una consulta nueva sobre la colección de datos', 
                        'Hacer wiki crawler', 
                        'Imprimir la información de los desarrolladores', 
                        'Imprimir la información de la aplicación'))

if status == 'Procesar las consultas de la colección de datos':
    option = 1
elif status == 'Realizar una consulta nueva sobre la colección de datos':
    option = 2
elif status == 'Hacer wiki crawler':
    option = 3
elif status == 'Imprimir la información de los desarrolladores':
    option = 4
elif status == 'Imprimir la información de la aplicación':
    option = 5

if option == 1:
    st.header('Solo hay consultas personalizadas para el modelo vectorial')
    st.subheader('Escoja la colección de datos deseada')
    corpus = st.radio('', ('CRANFIELD', 'CISI'))

    if corpus == 'CRANFIELD':
        if st.button('Aceptar'):
            cranfield_app()
            st.success('Terminado exitosamente!')
    else:
        if st.button('Aceptar'):
            cisi_app()
            st.success('Terminado exitosamente!')

elif option == 2:
    st.header('Escoja el modelo a desarrollar')
    model = st.radio('', ('Booleano', 'Vectorial'))

    if model == 'Booleano':
        st.header('Escoja la colección de datos deseada')
        corpus = st.radio('', ('CRANFIELD', 'CISI'))

        if corpus == 'CRANFIELD':
            booleanModel('../collections/cranfield/cran.all.1400')
        else:
            booleanModel('../collections/cisi/cisi.all')
    else:
        st.header('Escoja la colección de datos deseada')
        corpus = st.radio('', ('CRANFIELD', 'CISI'))

        if corpus == 'CRANFIELD':
            st.subheader('Escriba la consulta deseada')
            query = st.text_input(' ', ' ')

            if st.button('Aceptar'):
                cranfield_manual_query_app(query)
                st.success('Terminado exitosamente!')
        elif corpus == 'CISI':
            st.subheader('Escriba la consulta deseada')
            query = st.text_input(' ', ' ')

            if st.button('Aceptar'):
                cisi_manual_query_app(query)
                st.success('Terminado exitosamente!')
        else:
            pass

elif option == 3:
    st.header('Haciendo web crawler a sitios aleatorios de la wikipedia')
    done = WikiCrawler().crawl(10)

    if done:
        st.success('Terminado exitosamente!')
    else:
        st.error('Error!')

elif option == 4:
    st.header('Información de los Desarrolladores')
    st.write('Nombre y Apellidos : Thalia Blanco Figueras , Correo : lia.blanco98@gmail.com , Grupo : C512')
    st.write('Nombre y Apellidos : Eziel C. Ramos Piñón , Correo : ezielramos498@gmail.com , Grupo : C511')
    st.write('Nombre y Apellidos : Ariel Plasencia Díaz , Correo : arielplasencia00@gmail.com , Grupo : C512')

else:
    st.header('Información de la Aplicación')
    st.write('Sistema de Recuperación de Información v2.0')
    st.write('Copyright © 2022: Thalia Blanco, Eziel Ramos, Ariel Plasencia')
