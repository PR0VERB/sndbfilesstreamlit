# https://www.youtube.com/watch?v=aruInGd-m40&t=278s
# https://www.youtube.com/watch?v=H8Ars15wGRM
    #TODO Columns validation 
    # # TODO: make file type agnostic

import streamlit as st
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import datetime
import base64
# https://dash.plotly.com/dash-core-components/upload
import io
from src import (
    upload_files_to_gdrive,
    list_out_file_from_gdrive,
    download_files_from_gdrive,
    create_file_and_write_text_init,
    )

# hide the header and footer #
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
# hide the header and footer #

                                                                        ######################### 1. Import UPLOADING Libraries ####################


# try:
# with st.forms()
stake_df= pd.read_excel('DATA/stakes_df.xlsx')
stake_addresses = list(stake_df['Email Address'])
stake_addresses = [address.lower() for address in stake_addresses]
    # verify email
enter_email = st.text_input("Please enter your email address", value="")
enter_email = enter_email.lower()
email_verify_button = st.button("Verify Email Address")

# if email_verify_button: 
if enter_email in stake_addresses: #because if email_verify_button: does not work

    st.success('✔ **Email address verified**')
    
    drive_directory_df = pd.read_excel('DATA/GoogleDriveIndicatorMetroFolderID.xlsx', sheet_name='main')
    
    # metro list
    metros = list(drive_directory_df.Metro.unique())
    metros.insert(0,'Make a Selection')
    # indicator list
    indicators = list(drive_directory_df.Indicator.unique())
    indicators.insert(0,'Make a Selection')
    st.write("before metro selected")
    metro_selected = st.selectbox("Select a metro", tuple(metros), key=1)
    if metro_selected != 'Make a Selection':
        st.write("before idncatpr selected")
        indicator_selected = st.selectbox("Select an indicator", tuple(indicators), key = 2)
        
        
        if indicator_selected != 'Make a Selection':
            def update_logs(file_name:str):
                log_df = pd.DataFrame(columns = ['Timestamp', 'ID', 'Date', 'FileName'], dtype = object) # replace with db
                timestamp = time.time()
                #IDs = log_df['Timestamp    '].str().strip()
                id = str(timestamp)
                date = datetime.date.today()
                file_name = file_name
                log_df.loc[len(log_df.index)] = [timestamp, id, date, file_name]
                return log_df
            

                                                                        ######################### 2. UPLOADING to Streamlit then to csv #########################
            
            uploaded_file = st.file_uploader("Choose an xlsx or csv file")
            if uploaded_file is not None:
                file_dir = "DATA/"
                file_path = f"{file_dir}{uploaded_file.name}"
                folder_id = drive_directory_df[(drive_directory_df.Metro == metro_selected) & (drive_directory_df.Indicator == indicator_selected)].FolderID.values[0]
                
                if 'xls' in uploaded_file.name:
                    def chosen_sheet(uploaded_file: str):
                        return pd.read_excel(uploaded_file,sheet_name= None)
                    df_ = chosen_sheet(uploaded_file)
                    chosen_sheet = st.selectbox('Please choose sheet name', (df_.keys()))
                    st.write('Your selected sheet:', chosen_sheet)
                    df = pd.read_excel(uploaded_file, sheet_name= chosen_sheet)
                    # 3. take the dataframe to excel and save to file directory 
                    df.to_excel(file_path)
                    save_as_name = f'SHEET_{chosen_sheet}_FILE_{uploaded_file.name}'
                    display_name = f"{uploaded_file.name}: {chosen_sheet} uploaded to database"
                    
                elif 'csv' in uploaded_file.name:
                    df = pd.read_csv(uploaded_file)
                    df.to_csv(file_path)
                    save_as_name = f'{uploaded_file.name}'
                    display_name = f"{save_as_name} uploaded to database"
                    
                # display short df
                df_top_bottom = pd.concat([df.head(5),df.tail(5)], axis = 0).sort_index()
                del df
                file_name = uploaded_file.name
                st.write(df_top_bottom)
                log_df = update_logs(file_name)
                log_df.to_csv("log_csv.csv", index=False)
                
                gauth = GoogleAuth()           
                drive = GoogleDrive(gauth)
                if st.button("Click to upload"):
                    gfile = upload_files_to_gdrive([file_path], drive, folder_id)
                    st.write(display_name)
                    gfile['title'] = save_as_name # Change title of the file.
                    gfile.Upload() # Update metadata.# rename file
            else: 
                st.write("File will be uploaded once you have completed the fields above")
            
                                                                                                ################3. pydrive########################

elif email_verify_button and enter_email not in stake_addresses:
    st.write('It seems like your email address does not appear have access to this plaform. Please contact Bill - bseota@gmail.com and request to be added to the database.')
    
