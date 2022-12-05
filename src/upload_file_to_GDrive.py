# Get Authentication for Google Service API through the attached PDF.
# Download client_secrets.json from Google API Console and OAuth2.0 is done in two lines.
# You can customize the behavior of OAuth2 in one settings file settings.yaml
# upload file to google drive and add the file in list you want to upload
def upload_files_to_gdrive(upload_file_list, drive, driveId):
    for upload_file in upload_file_list:
        gfile = drive.CreateFile(
            {'parents': [{'id': driveId}]})
        # Read file and set it as the content of this instance.
        gfile.SetContentFile(upload_file)
        gfile.Upload() # Upload the file.
    return gfile