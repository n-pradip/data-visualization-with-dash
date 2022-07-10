# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
# import sqlalchemy


app = Dash(__name__)

# reading data from database
# engine = sqlalchemy.create_engine('postgresql://--username here--:--password here--@localhost:5432/--db name--')
# df = pd.read_sql_query("select * from user_marks", con=engine)

# reading data from csv file
df = pd.read_csv(r"student_dataset.csv")

# replacing the data values in id with respective user values in string 
df['exam_id'] = df['exam_id'].replace([1],'first_term_examination')
df['student_id'] = df['student_id'].replace([1],'ram')
df['student_id'] = df['student_id'].replace([2],'shyam')
df['student_id'] = df['student_id'].replace([3],'gita')
df['student_id'] = df['student_id'].replace([4],'Sarita')
df['student_id'] = df['student_id'].replace([5],'pradip')

df['subject_id'] = df['subject_id'].replace([1],'Nepali')
df['subject_id'] = df['subject_id'].replace([2],'English')
df['subject_id'] = df['subject_id'].replace([4],'Maths')
df['subject_id'] = df['subject_id'].replace([5],'Science')
df['subject_id'] = df['subject_id'].replace([6],'Social')


# making filter objects 
filt_nep = (df["subject_id"]=="Nepali")
filt_eng = (df["subject_id"]=="English")
filt_mat = (df["subject_id"]=="Maths")
filt_sci = (df["subject_id"]=="Science")
filt_social = (df["subject_id"]=="Social")

nepali_only_results = df[filt_nep]
english_only_results = df[filt_eng]
maths_only_results = df[filt_mat]
science_only_results = df[filt_sci]
social_only_results = df[filt_social]

# Students name column  
filt_names = df["student_id"]
names = filt_names.unique().tolist()

# making list of each subject marks
nepali_marks = nepali_only_results['marks'].tolist()
english_marks = english_only_results['marks'].tolist()
science_marks = science_only_results['marks'].tolist()
maths_marks = maths_only_results['marks'].tolist()
social_marks = social_only_results['marks'].tolist()

# Making master dataframe concatinating the each subject marks
master_dataframe = {'Students':names,'Nepali':nepali_marks,'English':english_marks,'Science':science_marks,'Maths':maths_marks,'Social':social_marks}


fig = px.line(master_dataframe, x="Students", y=['Nepali', 'English', 'Science', 'Maths', 'Social'], 
              markers=True, 
              title='Students and their performance(marks) in first terminal examination',
              labels={"value":"Marks","full_name": "Students","variable": "Subjects"}
              )

# for percentage of each student
filt = df["student_id"]=="gita"
total_marks = df[filt]["marks"].sum()
percentage = (total_marks/500)*100

fig_each_student =  px.bar(df[filt], x="subject_id", y="marks", title="Each student first_terminal_examination progress", width=800, height=600, range_y=(0,100))



app.layout = html.Div(children=[
    html.H1(children='Students data'),

    html.Div(children='''
        Showing dataframe for comparative results of students between marks and subjects
    '''),

    html.Br(),

    # dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]),   ==> easy table oneliner

    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        virtualization=True,
        fixed_rows={'headers': True},
        style_header = {
            # 'backgroundColor': '#191970',
            'color': '#191970',
            'fontWeight': 'bold',
            'fontSize':'16px',
        },
        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
        style_table={'height': 300}  # default is 500
),
    

    dcc.Graph( 
        figure=fig
    ),

    html.H3(children='Filter/select student to view each student data'),

    html.Div([
    dcc.Dropdown(names, names[0],id='each_student_info_inputid')   #name here is the list of student name from database
    ]),

    html.Br(),
    html.Div(['{{student}} got percentage in first_terminal examination'],id="output_id"),

    html.Div(dcc.Graph(id='bar_graph'),style={'display': 'inline-block'}),

    html.Div(dcc.Graph(id='pie_chart'),style={'display': 'inline-block'}),

])


# Callback for the student=> percentage statement
@app.callback(
    Output(component_id='output_id', component_property='children'),
    Input(component_id='each_student_info_inputid', component_property='value')
)

def get_individual_percentage(each_student_info_inputid):
    student_name = each_student_info_inputid
    filt = df["student_id"]==str(each_student_info_inputid)
    total_marks = df[filt]["marks"].sum()
    percentage = "{:.2f}".format((total_marks/500)*100)
    return f'{student_name} got {percentage}% in first_terminal_examination.'


# Callback for bargraph of individual student with dropdown value as input
@app.callback(
    Output(component_id='bar_graph', component_property='figure'),
    Input(component_id='each_student_info_inputid', component_property='value')
)
def get_indivigual_bar_graph(each_student_info_inputid):
    filt = df["student_id"]==str(each_student_info_inputid)
    fig =  px.bar(df[filt], x="subject_id", y="marks", title=f"{each_student_info_inputid}'s first_terminal_examination progress report", width=800, height=600, range_y=(0,100))
    return fig


# Callback for piechart of individual student with dropdown value as input
@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    Input(component_id='each_student_info_inputid', component_property='value')
)
def get_indivigual_pie_chart(each_student_info_inputid):
    filt = df["student_id"]==str(each_student_info_inputid)
    fig =  px.pie(df[filt], names = 'subject_id', values='marks', title=f"Contribution of each subject in overall examination percentage" , width=800, height=600)
    fig.update_traces(textinfo='value')
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)