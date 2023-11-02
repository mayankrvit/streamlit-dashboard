#import sqlserver.connector
#import streamlit as st 

# import pypyodbc
# Driver_name = 'SQL SERVER'
# SERVER_NAME = 'DESKTOP-P2ASTGM\SQLEXPRESS'
# Database_name = 'Insurance_data'

# connection_string = f"""
#     DRIVER ={{{Driver_name}}};
#     SERVER ={{{SERVER_NAME}}};
#     DATABASE ={{{Database_name}}};
#     Trust_Connection = yes;
# """
    
# conn = pypyodbc.connect(connection_string)

import pypyodbc

connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=DESKTOP-P2ASTGM\SQLEXPRESS;Database=Insurance_data;Trusted_Connection=yes;"

# Establish the connection
conn = pypyodbc.connect(connection_string)

# Perform your database operations here

# Close the connection
# conn.close()

# short way of query rows = conn.cursor().execute(sql_query).fetchall()

sql_query  = "select * from ins_data"

cursor = conn.cursor()
cursor.execute(sql_query)
rows = cursor.fetchall()
columns = [column[0] for column in cursor.description]

import pandas as pd
df = pd.DataFrame(rows, columns= columns)


pd.set_option('display.max_column', None)










