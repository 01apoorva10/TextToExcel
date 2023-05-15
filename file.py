import pandas as pd
import streamlit as st
from io import BytesIO
import urllib.parse
import os

import pandas as pd

def process_text_file(file):
    data = pd.read_csv(file, header=None)
    data.columns = ["PipeRun", "Position X(M)", "Position Y(M)", "Position Z(M)", "Support Tag"]
    
    # Splitting the values in Column1
    split_values = data['PipeRun'].str.split('-', n=3).str[:3].str.join('-')
    data['Pipeline'] = split_values
    data = data.assign(PipePart="Pipe")
    data = data.assign(Structure_Member="Nill")
    data = data.assign(Direction="N")
    data = data.assign(Support_Part_No="LogicalPoint")
    desired_order = ['Pipeline','PipeRun','PipePart','Structure_Member','Direction','Support_Part_No','Support Tag','Position X(M)', 'Position Y(M)', 'Position Z(M)']
    data = data.reindex(columns=desired_order)
    data.index.name = 'SNO'
    data.index+=1
    data.drop_duplicates(inplace=True)
    data["PipeRun"]= data["PipeRun"].apply(lambda x: x.replace('IN','"'))
    data["PipeRun"]= data["PipeRun"].apply(lambda x: x.replace('0.5','1/2'))
    data["PipeRun"]= data["PipeRun"].apply(lambda x: x.replace('0.75','3/4'))
    data["PipeRun"]= data["PipeRun"].apply(lambda x: x.replace('1.5','1-1/2'))
    preview = data[['Pipeline','PipeRun','PipePart','Structure_Member','Direction','Support_Part_No','Support Tag','Position X(M)', 'Position Y(M)', 'Position Z(M)']]
    
    return data, preview

def download_excel_file(data, file_name):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, sheet_name='Sheet1', index=False)
    output.seek(0)
    
    base_name = os.path.splitext(file_name)[0]
    excel_file_name = base_name + ".xlsx"
    quoted_file_name = urllib.parse.quote(excel_file_name)  # Encode file name for URL
    return output, quoted_file_name




# Streamlit app
# Streamlit app
def main():
    
    
    
    st.markdown("<h2 style='font-style:italic ; font-family: Times New Roman ; text-align: center '>PipeSupport Data Generator </h2>", unsafe_allow_html=True)

    # Sidebar - File Upload
    st.sidebar.markdown("<h3 style='font-style:italic'>Upload a text file</h3>", unsafe_allow_html=True)
    file = st.sidebar.file_uploader("", type="txt")

    # Main content - Preview and Download
    # st.markdown("<h3 style='font-style:italic'>Preview of the first column:</h3>", unsafe_allow_html=True)
    if file is not None:
        data, preview = process_text_file(file)
        st.write(preview)

        text_file_name = file.name
        excel_file, file_name = download_excel_file(data, text_file_name)
        # st.markdown("<h3 style='font-style:italic'>Download PipeSupport Data</h3>", unsafe_allow_html=True)
        st.download_button("Download", excel_file, file_name=file_name, mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    main()