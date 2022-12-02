# https://www.youtube.com/watch?v=aruInGd-m40&t=278s
# https://www.youtube.com/watch?v=H8Ars15wGRM

import streamlit as st
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
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

######################### Import UPLOADING Libraries ####################


# initialise stakeholder dataframe
try:
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
    #     print("")
    #     # st.write('It seems like your email address does not have access to this plaform. Please contact Bill - bseota@gmail.com and request to be added to the database.')
    # else:
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
                # st.write("before upload")
                uploaded_file = st.file_uploader("Choose an xlsx or csv file")
                # if uploaded_file is not None:
                #     def chosen_sheet(uploaded_file: str):
                #         return pd.read_excel(uploaded_file,sheet_name = 'Sheet1')
                #     df_ = chosen_sheet(uploaded_file)
                # print("UPLOADED FILE ##############################", uploaded_file)
                #assign the corresponding folder id
                folder_id = drive_directory_df[(drive_directory_df.Metro == metro_selected) & (drive_directory_df.Indicator == indicator_selected)].FolderID.values[0]
        #TODO Columns validation 
        # print("UPLOADED FILE ##############################", uploaded_file)

        # # TODO: make file type agnostic
                                                                ######################### UPLOADING #########################

        # 1. get the current working directory
        # file_dir = os.getcwd()
        file_dir = "DATA/"
        # 2. append current working directory to the file name
        # file_path = os.path.join(file_dir,uploaded_file.name)
        file_path = f"{file_dir}{uploaded_file.name}"
        st.write(file_path)
        # 3. take the dataframe to excel and save to file directory 
        # df_.to_excel(file_path)
        # del df_
        
        print("Backed up file" + uploaded_file.name)
        
        ################pydrive########################
        gauth = GoogleAuth()           
        drive = GoogleDrive(gauth)

        upload_files_to_gdrive([file_path], drive, folder_id)#
        print("uploaded")
    elif email_verify_button and enter_email not in stake_addresses:
        st.write('It seems like your email address does not appear have access to this plaform. Please contact Bill - bseota@gmail.com and request to be added to the database.')
        
    ################pydrive########################
            
except:
    pass

                                                        ######################### end UPLOADING #########################
