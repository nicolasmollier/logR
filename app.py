import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

from src.project_utils.io import get_newest_file_path

pio.templates.default = "plotly_white"
st.set_page_config(layout="wide")

latest_log_file, log_file_paths = get_newest_file_path("data")
default_ix = log_file_paths.index(latest_log_file)

with st.sidebar:
    selected_log_file = st.selectbox(
       label="Log file:",
       label_visibility="visible",
       options=log_file_paths,
       index=None,  # default_ix
       placeholder="Select a log file:",
    )
# st.write('You selected:', selected_log_file)

# file_upload = st.file_uploader("Choose a log-file")

#if file_upload:
#    log_df = pd.read_csv(file_upload)
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

    fig = px.line(log_df_long, x="time", y="value", color="parameter")
    fig.update_layout(
        legend=dict(orientation="h"),
        legend_title=None,
        hovermode='x unified',
    )
    fig.update_xaxes(title=None, showticklabels=False)
    fig.update_traces(visible="legendonly", selector=lambda t: not t.name in selected_parameters)
    for trace in fig['data']:
        if (not trace['name'] in selected_parameters):
            trace['showlegend'] = False
    st.plotly_chart(fig, use_container_width=True)

