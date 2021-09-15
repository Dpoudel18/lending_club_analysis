import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load dataset
df = pd.read_csv("data/lending_club_modified_data.csv", index_col=False, dtype='unicode')

df = df.copy(deep=True).astype({'emp_length_years': 'int64'})

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
    #fig.update_layout(title=title_name,title_x=0.5)

    # play around with the font and its size of the body
    fig.update_layout(font_family="Arial", font_size = 15)

    # play around with the font and its size of the title
    fig.update_layout(title = {'font_color':'#e75480', 'font_size':25})

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
st.markdown("<h1 style='text-align: center'>Good Loans and Bad Loans</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center'>Exploratory Data Analysis of<a href = https://www.kaggle.com/puneeshk/lending-loan-club-dataset target=_blank> Lending Club Loan Dataset</a></p>", unsafe_allow_html=True)


options = ['Choose from Options','Loan Status', 'Loan Type', 'Loan Segment by Term', 'Loan Segment by Grade', "Employment Duration and Loan Type", "Borrower's Employer and Good Loan", "Purpose for Bad Loans"]
st.markdown("## What do you want to discover about?")
page = st.selectbox("", options)

if page == 'Choose from Options':
    st.sidebar.markdown("## What is 'Good Loans'?")
    st.sidebar.markdown('Loans with status of "Current", "Issued" or "Fully Paid".')
    st.sidebar.markdown("## What is 'Bad Loans'?")
    st.sidebar.markdown('Loans with status other than "Current", "Issued" or "Fully Paid".')
    #st.markdown("## Loan Status in Lending Club:")
    st.sidebar.markdown("## Questions to discover:")
    st.sidebar.markdown("- What proportion of loans are 'Good Loans/Bad Loans' based on term?")
    st.sidebar.markdown("- What proportion of loans are 'Good Loans/Bad Loans' based on grade?")
    st.sidebar.markdown("- Is 'Good Loans' somehow linked with the job of the borrowers?")
    st.sidebar.markdown("- Is 'Good Loans' somehow linked with the job duration of the borrowers?")
    st.sidebar.markdown("- What are the most frequent purpose values for 'Bad Loans'?")

# Loan Status
if page == 'Loan Status':

    st.markdown(
        """## <a style='display: block; text-align: center'>Loan Status in Lending Club</a>
        """,
        unsafe_allow_html=True,
    )
    loan_status_df = build_df('loan_status')
    st.write('')
    st.sidebar.markdown(
        """## <a style='display: block; text-align: center'>Loan Status</a>
        """,
        unsafe_allow_html=True,
    )
    #st.table(loan_status_df.assign(hack='').set_index('hack'))
    st.sidebar.table(loan_status_df.assign(hack='').set_index('hack'))
    
    loan_status_type = loan_status_df['loan_status']
    loan_status_count = loan_status_df['count']
    fig = plot_pretty_pie_chart(loan_status_type, loan_status_count, 'Loan Status')
    st.plotly_chart(fig)

    st.sidebar.markdown("Out of 39717 data points, the loan status consists of:")
    st.sidebar.markdown('- 32,950 fully paid (83%)')
    st.sidebar.markdown('-  5,627 charged off (14.2%)')
    st.sidebar.markdown("-  1,140 current (2.87%)")


#  Loan Type 
if page == 'Loan Type':

    st.markdown(
        """## <a style='display: block; text-align: center'>Loan Type in Lending Club</a>
        """,
        unsafe_allow_html=True,
    )
    loan_type_df = build_df('loan_type')
    st.write('')
    #st.table(loan_type_df.assign(hack='').set_index('hack'))
    st.sidebar.markdown(
        """## <a style='display: block; text-align: center'>Loan Type</a>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.table(loan_type_df.assign(hack='').set_index('hack'))
    loan_type = loan_type_df['loan_type']
    loan_type_count = loan_type_df['count']
    fig = plot_pretty_pie_chart(loan_type, loan_type_count, 'Loan Type')
    st.plotly_chart(fig)
    st.sidebar.markdown("Out of 39717 data points, the loan type consists of:")
    st.sidebar.markdown("- 34,090 'Good Loans' (85.8%)")
    st.sidebar.markdown("-  5,627 'Bad Loans' (14.2%)")

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
    fig.update_layout(width=700, height=650)
    fig.update_layout()
    #fig.update_layout(title=title_name,title_x=0.5)
    fig.update_layout(legend_title_text='Loan type')
    fig.update_layout(font_family="Arial", font_size = 15)
    fig.update_layout(title = {'font_color':'pink', 'font_size':25})
    return fig

# Loan segment by term
if page == "Loan Segment by Term":
    
    loan_segment_by_term_df = generate_df_by_segment_column('term').reset_index()
    st.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Term (Count)</a>
    """,
    unsafe_allow_html=True,
    )
    st.sidebar.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Term (Count)</a>
    """,
    unsafe_allow_html=True,
    )
    st.sidebar.table(loan_segment_by_term_df[['term','loan_type','count']].assign(hack='').set_index('hack'))

    st.sidebar.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Term (%)</a>
    """,
    unsafe_allow_html=True,
    )
    st.sidebar.table(loan_segment_by_term_df[['term','loan_type','percent']].assign(hack='').set_index('hack'))

    fig = plot_grouped_bar_chart(loan_segment_by_term_df, 'term', 'count', 'loan_type','Loan Segment by Term (Total)')
    st.plotly_chart(fig)

    fig2 = plot_grouped_bar_chart(loan_segment_by_term_df, 'term', 'percent', 'loan_type','Loan Segment by Term (%)')

    st.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Term (%)</a>
    """,
    unsafe_allow_html=True,
    )

    st.plotly_chart(fig2)

    st.sidebar.markdown("For the term of 36 months, the loans constitutes of:")
    st.sidebar.markdown("- 25,869 'Good Loans' (89%)")
    st.sidebar.markdown("-  3,227 'Bad Loans' (11%)")

    st.sidebar.markdown("For the term of 60 months, the loans constitutes of:")
    st.sidebar.markdown("- 8,221 'Good Loans' (77%)")
    st.sidebar.markdown("-  2,400 'Bad Loans' (23%)")
    st.markdown("<u>Observations:</u>",unsafe_allow_html=True)
    st.markdown("- As we can notice, comparing the proportion, the 60 months term welcomes more 'Bad Loans' (almost twice).")
    st.markdown("- The 36 months term loan has a high count of 'Good Loans' as well low rate of 'Bad Loans'. Hence, it is beneficial for the firm to keep prioritizing this option.")



# Loan segment by Grade
if page == "Loan Segment by Grade":
    
    
    loan_segment_by_grade_df = generate_df_by_segment_column('grade').reset_index()
    st.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Grade (Count)</a>
    """,
    unsafe_allow_html=True,
    )
    st.sidebar.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Grade (Count)</a>
    """,
    unsafe_allow_html=True,
    )
    st.sidebar.table(loan_segment_by_grade_df[['grade','loan_type','count']].assign(hack='').set_index('hack'))

    st.sidebar.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Grade (%)</a>
    """,
    unsafe_allow_html=True,
    )
    st.sidebar.table(loan_segment_by_grade_df[['grade','loan_type','percent']].assign(hack='').set_index('hack'))

    fig = plot_grouped_bar_chart(loan_segment_by_grade_df, 'grade', 'count', 'loan_type','Loan Segment by Grade (Count)')
    st.plotly_chart(fig)

    fig2 = plot_grouped_bar_chart(loan_segment_by_grade_df, 'grade', 'percent', 'loan_type','Loan Segment by Grade (%)')

    st.markdown(
    """## <a style='display: block; text-align: center'>Loan Segment by Grade (%)</a>
    """,
    unsafe_allow_html=True,
    )

    st.plotly_chart(fig2)
    st.markdown("<u>Observations:</u>",unsafe_allow_html=True)
    st.markdown("- Majority of the loans issued have grade of A and B (almost 50%), which is good for the company.")
    st.markdown("- The grade F and G are bad for the company with the default rate of 30% and 32% respectively.")
    st.markdown("- Like it should be, the higher the grade, the less the percentage of 'Bad Loans' and vice-versa.")

#df = df.copy(deep=True).astype({'emp_length_years': 'int64'})


# helper functions to get good loan df
def get_segmented_good_loan_df(var_name):
    data = generate_df_by_segment_column(var_name).reset_index()
    data = data[data['loan_type']=='Good Loans']
    return data

# helper functions to get bad loan df
def get_segmented_bad_loan_df(var_name):
    data = generate_df_by_segment_column(var_name).reset_index()
    data = data[data['loan_type']=='Bad Loans']
    return data

# helper function to plot line chart
def plot_line_chart(data, x_value, y_value, title_name,color):
    df = data.reset_index()
    fig = px.line(data_frame=df, x=x_value, y=y_value, labels={
                        x_value: 'Employment Length (Years)',
                        y_value: 'Percent'
                    }, hover_data = {'percent':True,'count':True},color_discrete_sequence=[color], orientation='h')

    fig.update_layout(width=800, height=750)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    #fig.update_layout(title=title_name,title_x=0.5)
    #fig.update_layout(legend_title_text='Loan type')
    fig.update_layout(font_family="Times New Roman", font_size = 15)
    #fig.update_layout(title = {'font_color':'pink', 'font_size':25})
    return fig


# Borrower's Employer and Good Loan
if page == "Borrower's Employer and Good Loan": 
    new_df = dict(df[df['loan_type']=='Good Loans']['emp_title'].value_counts())
    good_loan_employer_df = pd.DataFrame(new_df.items(),columns = ['emp_title','count']).head(16)
    st.markdown(
    """## <a style='display: block; text-align: center'>Borrower's Employer and Good Loan</a>
    """,
    unsafe_allow_html=True,
    )
    st.table(good_loan_employer_df.assign(hack='').set_index('hack'))
    st.markdown("<u>Observations:</u>",unsafe_allow_html=True)
    st.markdown('- Since the column emp_title is composed from an open ended question, this is not a categorical column and not much could be deduced from it.')
    st.markdown('- However, it is interesting to observe that most of the borrowers belong to U.S. Military and big corporations.')



# Employment Duration and Loan Type
if page == "Employment Duration and Loan Type":  
    emp_length_good_loan_df = generate_df_by_segment_column('emp_length_years').reset_index()
    emp_length_good_loan_df = emp_length_good_loan_df[emp_length_good_loan_df['loan_type']=='Good Loans']
    emp_length_good_loan_df = emp_length_good_loan_df.reset_index(drop=True)
    st.markdown(
    """## <a style='display: block; text-align: center'>Employment Duration and Good Loan</a>
    """,
    unsafe_allow_html=True,
    )
    st.table(emp_length_good_loan_df.assign(hack='').set_index('hack'))
    fig3 = plot_line_chart(emp_length_good_loan_df, 'emp_length_years', 'percent','Good Loan and Employment Duration','pink')
    st.markdown("<u>Note:</u>", unsafe_allow_html= True)
    st.markdown(' - -1 in the dataframe corresponds to number of missing data in *emp_length_years* columns.')
    st.markdown(' - 0 in the dataframe corresponds to less than 1 year.')
    st.markdown(' - 10 in the dataframe corresponds to 10 or more years.', unsafe_allow_html=True)
    st.markdown(
    """## <a style='display: block; text-align: center'>Employment Duration and Good Loan (%)</a>
    """,
    unsafe_allow_html=True,
    )
    st.plotly_chart(fig3)
    emp_length_bad_loan_df = generate_df_by_segment_column('emp_length_years').reset_index()
    emp_length_bad_loan_df = emp_length_bad_loan_df[emp_length_bad_loan_df['loan_type']=='Bad Loans']
    emp_length_bad_loan_df = emp_length_bad_loan_df.reset_index(drop=True)
    st.markdown(
    """## <a style='display: block; text-align: center'>Employment Duration and Good Loan (Count)</a>
    """,
    unsafe_allow_html=True,
    )
    #st.table(emp_length_bad_loan_df.assign(hack='').set_index('hack'))
    fig4 = plot_line_chart(emp_length_bad_loan_df, 'emp_length_years', 'count','Bad Loan and Employment Duration','maroon')    
    st.plotly_chart(fig4)
    st.markdown("<u>Observations:</u>",unsafe_allow_html=True)
    st.markdown("- The lowest percentage of 'Good Loans' or the highest percentage of 'Bad Loans' exist in the category of missing values where people don't report their employment length. It is highly likely they don't have a job to pay their loans on time.") 
    st.markdown("- Also 'Good Loans' seems to be significant higher in 10+ years of employment category.")

if page == "Purpose for Bad Loans":
    bad_loan_purpose_df = get_segmented_bad_loan_df('purpose').reset_index(drop=True).sort_values(by=['percent'], ascending=False)
    st.markdown(
    """## <a style='display: block; text-align: center'>Purpose for Bad Loans</a>
    """,
    unsafe_allow_html=True,
    )
    st.table(bad_loan_purpose_df.assign(hack='').set_index('hack'))
    #st.write(bad_loan_purpose_df.assign(hack='').set_index('hack'))
    fig = px.bar(bad_loan_purpose_df, x="percent", y="purpose", labels={
                        'percent': 'Percent',
                        'purpose': 'Purpose'}, orientation='h', hover_data = {'count':True})
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.update_layout(width=800, height=750)
    fig.update_traces(marker_color='maroon')
    fig.update_layout(font_family="Arial", font_size = 15)
    #fig.update_layout(title='Purpose for Bad Loans (%)',title_x=0.5)
    #fig.update_layout(title = {'font_color':'maroon', 'font_size':25})
    st.markdown(
    """## <a style='display: block; text-align: center'>Purpose for Bad Loans (Percent)</a>
    """,
    unsafe_allow_html=True,
    )
    st.plotly_chart(fig)
    bad_loan_purpose_df = get_segmented_bad_loan_df('purpose').reset_index(drop=True).sort_values(by=['count'], ascending=False)
    fig = px.bar(bad_loan_purpose_df, x="count", y="purpose", labels={
                        'count': 'Count',
                        'purpose': 'Purpose'}, orientation='h', hover_data = {'count':True})
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.update_layout(width=800, height=750)
    fig.update_traces(marker_color='maroon')
    fig.update_layout(font_family="Arial", font_size = 15)
    #fig.update_layout(title='Purpose for Bad Loans (Total)',title_x=0.5)
    #fig.update_layout(title = {'font_color':'maroon', 'font_size':25})
    st.markdown(
    """## <a style='display: block; text-align: center'>Purpose for Bad Loans (Count)</a>
    """,
    unsafe_allow_html=True,
    )
    st.plotly_chart(fig)
    st.markdown("<u>Observations:</u>",unsafe_allow_html=True)
    st.markdown("- Debt Consolidation seems to be way ahead in terms of total count.")
    st.markdown("- It is not surprising to see that the main purpose for 'Bad Loans' in terms of proportion is for small business purpose with 26%. Small businesses often involve a lot of risks with poor cash flow.")
    st.markdown("- Renewable energy sits at the second spot. However, the count for renewable energy loans is only 19. Hence, it is still too early to decipher something out of it.")
    st.markdown("- Educational purpose is also not surpising to see since it is more of a long-term investment.")
    st.markdown("- Looks like the option 'other' is also prone to 'Bad Loans'.")
