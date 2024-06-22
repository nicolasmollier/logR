import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

from src.project_utils.io import get_newest_file_path

pio.templates.default = "plotly_white"
st.set_page_config(layout="wide")

latest_log_file, log_file_paths = get_newest_file_path("data")
default_ix = log_file_paths.index(latest_log_file)

if 'options' not in st.session_state:
    st.session_state.options = log_file_paths

if 'file_upload_path' not in st.session_state:
    st.session_state.file_upload_path = None
    st.write(st.session_state.file_upload_path)

def update_options():
    # move the selected option to the front of the list if it is not already
    if st.session_state.file_upload_path not in st.session_state.options:
        st.session_state.options.insert(0, st.session_state.file_upload_path)
        st.write(st.session_state.options)

with st.sidebar:
    selected_log_file = st.selectbox(
       label="Log file:",
       label_visibility="visible",
       options=st.session_state.options,
       index=None,  # default_ix
       placeholder="Select a log file:",
       key="selected_option",
       on_change=update_options,
    )

if selected_log_file:
    log_df = pd.read_csv(selected_log_file)
    log_df.columns = log_df.columns.str.lower()
    log_df_long = pd.melt(log_df, id_vars="time", var_name="parameter", value_name="value")

    parameter_options = [parameter for parameter in log_df_long.parameter.unique() if not parameter.startswith("mhd")]
    with st.sidebar:
        selected_parameters = st.multiselect(
            label="Parameters:",
            label_visibility="visible",
            options=parameter_options,
            placeholder="Select parameters to plot",
        )
        file_upload = st.file_uploader("Upload a log-file", on_change=update_options)
        if file_upload is not None:
            st.session_state.file_upload_path = os.path.join("data", file_upload.name)
            with open(st.session_state.file_upload_path, "wb") as f:
                f.write(file_upload.getbuffer())
            st.success("Saved File")

    fig = px.line(log_df_long, x="time", y="value", color="parameter")
    fig.update_layout(
        legend=dict(orientation="h"),
        legend_title=None,
        hovermode='x unified',
    )
    fig.update_xaxes(title=None, showticklabels=False)
    fig.update_traces(visible="legendonly", selector=lambda t: not t.name in selected_parameters)
    for trace in fig['data']:
        if not trace['name'] in selected_parameters:
            trace['showlegend'] = False
    st.plotly_chart(fig, use_container_width=True)

