import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy
import numpy as np

# Load dataset
df = pd.read_csv("lending_club_modified_data.csv", index_col=False, dtype='unicode')


# function to create dataframe for pie chart
def build_df(var_name):

    # group the data based on var_name and store it as a dictionary
    data = dict(df[var_name].value_counts())

    # convert dictionary to pandas dataframe
    data = pd.DataFrame(data.items(),columns = [var_name,'count'])
    
    return data


# function to plot pie chart
def plot_pretty_pie_chart(label, value, title_name):

    # create a plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=label, values=value)])

    # write label and percentage inside/outside the chart
    fig.update_traces(textinfo='label+percent')

    # pull each pie slices a bit to make it look nicer
    fig.update_traces(pull=[0.1, 0.1, 0.1, 0.1])

    # assign bright color combinations
    fig.update_traces(marker=dict(colors=['#286086', 'maroon', 'blue']))

    # adjust the size of the figure 
    fig.update_layout(width=600, height=550)

    # give title to the chart and align it to the center
    fig.update_layout(title=title_name,title_x=0.5)

    # play around with the font and its size of the body
    fig.update_layout(font_family="Arial", font_size = 15)

    # play around with the font and its size of the title
    fig.update_layout(title = {'font_color':'white', 'font_size':25})

    # display the chart
    #fig.show()
    return fig

df = df.copy(deep=True).astype({'emp_length_years': 'int64'})










st.markdown("""
<style>
body {
    color: #zzz;
    background-color: #FFFFFF;
}
</style>
    """, unsafe_allow_html=True)
#st.title('Lending Club - Good Loans vs Bad Loans')
#st.markdown("## Lending Club Dataset")
st.markdown("<h1 style='text-align: center; color: Pink;'>Good Loans and Bad Loans: Lending Club</h1>", unsafe_allow_html=True)
st.sidebar.markdown("## What is 'Good Loans'?")
st.sidebar.markdown('Loans with status of "Current", "Issued" or "Fully Paid".')
st.sidebar.markdown("## What is 'Bad Loans'?")
st.sidebar.markdown('Loans with status other than "Current", "Issued" or "Fully Paid".')
#st.markdown("## Loan Status in Lending Club:")

options = ['Choose from Options','Loan Status', 'Loan Type', 'Loan Segment by Term', 'Loan Segment by Grade']
st.markdown("## What do you want to learn about?")
page = st.selectbox("", options)

# Loan Status
if page == 'Loan Status':

    st.markdown(
        """## <a style='display: block; text-align: center'>Loan Status in Lending Club</a>
        """,
        unsafe_allow_html=True,
    )
    loan_status_df = build_df('loan_status')
    st.write('')
    st.table(loan_status_df.assign(hack='').set_index('hack'))
    loan_status_type = loan_status_df['loan_status']
    loan_status_count = loan_status_df['count']
    fig = plot_pretty_pie_chart(loan_status_type, loan_status_count, 'Loan Status')
    st.plotly_chart(fig)

    st.markdown("### Out of 39717 data points, the loan status consist of:")
    st.markdown('- 32,950 fully paid (83%)')
    st.markdown('-  5,627 charged off (14.2%)')
    st.markdown("-  1,140 current (2.87%)")


#  Loan Type 
if page == 'Loan Type':

    st.markdown(
        """## <a style='display: block; text-align: center'>Loan Type in Lending Club</a>
        """,
        unsafe_allow_html=True,
    )
    loan_type_df = build_df('loan_type')
    st.write('')
    st.table(loan_type_df.assign(hack='').set_index('hack'))
    loan_type = loan_type_df['loan_type']
    loan_type_count = loan_type_df['count']
    fig = plot_pretty_pie_chart(loan_type, loan_type_count, 'Loan Type')
    st.plotly_chart(fig)
    st.markdown("### Out of 39717 data points, the loan type consist of:")
    st.markdown("- 34,090 'Good Loans' (85.8%)")
    st.markdown("-  5,627 'Bad Loans' (14.2%)")

#helper function
def generate_df_by_segment_column(segment_col):
    loan_segment_by_col_df = pd.DataFrame(df.groupby([segment_col,'loan_type'])['loan_type'].count())
    loan_segment_by_col_df['percent'] = loan_segment_by_col_df.groupby(level=0).apply(lambda x: round(100 * x / float(x.sum())))
    loan_segment_by_col_df = loan_segment_by_col_df.rename(columns={'loan_type':'count'})
    loan_segment_by_col_df['percent'] = loan_segment_by_col_df['percent'].apply(np.int64)
    return loan_segment_by_col_df

def plot_grouped_bar_chart(data, x_value, y_value, legend, title_name):
    df = data.reset_index()
    fig = px.bar(data_frame=df, x=x_value, y=y_value, color=legend, labels={
                    x_value: x_value.capitalize(),
                    y_value: y_value.capitalize()
                }, barmode="group", hover_data = {'percent':True,'count':True},color_discrete_sequence=['maroon','#286086'])
    fig.update_layout(width=600, height=550)
    fig.update_layout()
    fig.update_layout(title=title_name,title_x=0.5)
    fig.update_layout(legend_title_text='Loan type')
    fig.update_layout(font_family="Arial", font_size = 15)
    fig.update_layout(title = {'font_color':'white', 'font_size':25})
    return fig

# Loan segment by term
if page == "Loan Segment by Term":
    
    loan_segment_by_term_df = generate_df_by_segment_column('term').reset_index()
    st.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Term</a>
    """,
    unsafe_allow_html=True,
    )
    st.table(loan_segment_by_term_df.assign(hack='').set_index('hack'))

    fig = plot_grouped_bar_chart(loan_segment_by_term_df, 'term', 'count', 'loan_type','Loan Segment by Term (Total)')
    st.plotly_chart(fig)

    fig2 = plot_grouped_bar_chart(loan_segment_by_term_df, 'term', 'percent', 'loan_type','Loan Segment by Term (%)')
    st.plotly_chart(fig2)

    st.markdown("### For the term of 36 months, the loans constitutes of:")
    st.markdown("- 25,869 'Good Loans' (89%)")
    st.markdown("-  3,227 'Bad Loans' (11%)")

    st.markdown("### For the term of 60 months, the loans constitutes of:")
    st.markdown("- 8,221 'Good Loans' (77%)")
    st.markdown("-  2,400 'Bad Loans' (23%)")

    st.markdown("### As we can notice, the 60 months term welcomes more 'Bad Loans' in terms of proportion (almost twice).")

# Loan segment by Grade
if page == "Loan Segment by Grade":
    
    loan_segment_by_grade_df = generate_df_by_segment_column('grade').reset_index()
    st.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Grade</a>
    """,
    unsafe_allow_html=True,
    )
    st.table(loan_segment_by_grade_df.assign(hack='').set_index('hack'))

    fig = plot_grouped_bar_chart(loan_segment_by_grade_df, 'grade', 'count', 'loan_type','Loan Segment by Grade (Total)')
    st.plotly_chart(fig)

    fig2 = plot_grouped_bar_chart(loan_segment_by_grade_df, 'grade', 'percent', 'loan_type','Loan Segment by Grade (%)')
    st.plotly_chart(fig2)

    st.markdown("### For the term of 36 months, the loans constitute of:")
    st.markdown("- 25,869 'Good Loans' (89%)")
    st.markdown("-  3,227 'Bad Loans' (11%)")

    st.markdown("### For the term of 60 months, the loans constitute of:")
    st.markdown("- 8,221 'Good Loans' (77%)")
    st.markdown("-  2,400 'Bad Loans' (23%)")

    st.markdown("### As we can notice, the 60 months term welcomes more 'Bad Loans' in terms of proportion (almost twice).")
