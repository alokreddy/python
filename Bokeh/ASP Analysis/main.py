from os.path import dirname, join

import numpy as np
import pandas.io.sql as psql
import sqlite3 as sql

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc
from bokeh.sampledata.movies_data import movie_path

#conn = sql.connect(movie_path)
#query = open(join(dirname(__file__), 'query.sql')).read()
#movies = psql.read_sql(query, conn)
aspdf = pd.read_excel(r"India 2017 ASP as on 25-Sep-2017.xlsx")

#aspdf["color"] = np.where(aspdf["Oscars"] > 0, "orange", "grey")
#aspdf["alpha"] = np.where(aspdf["Oscars"] > 0, 0.9, 0.25)
aspdf.fillna(0, inplace=True)  # just replace missing values with zero
aspdf["Final Salary FTE"] = aspdf['Final Salary FTE'].apply(lambda x: '{:,d}'.format(int(x)))

#with open(join(dirname(__file__), "razzies-clean.csv")) as f:
#    razzies = f.read().splitlines()
#aspdf.loc[aspdf.imdbID.isin(razzies), "color"] = "purple"
#aspdf.loc[aspdf.imdbID.isin(razzies), "alpha"] = 0.9

aspdf['Last Hire Year'] = df['Last Hire Date'].dt.year
aspdf['Length of Service'] = datetime.datetime.now()

axis_map = {
    "Goals Rating": 'PDC Goals Rating',
    "HPC Rating": 'PDC HPC Rating',
    "Comp Ratio": "Comp Ratio",
    "Salary": "Final Salary FTE",
    "Service Length": "Length of Service",
    "Year": "Last Hire Year",
}

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)

# Create Input controls
reviews = Slider(title="Comp Ratio", value=80, start=10, end=300, step=10)
min_year = Slider(title="Year Hired", start=1940, end=2014, value=1970, step=1)
max_year = Slider(title="Final Salary FTE", start=1940, end=2014, value=2014, step=1)
oscars = Slider(title="Length of Service", start=0, end=4, value=0, step=1)
boxoffice = Slider(title="Salary", start=0, end=800, value=0, step=1)
genre = Select(title="Postion in Range", value="All",
               options=aspdf['Position in Range'].unique().tolist())
director = TextInput(title="Payroll Country Contains")
cast = TextInput(title="Manager Name")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Goals Rating")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="HPC Rating")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[], title=[], year=[], revenue=[], alpha=[]))

hover = HoverTool(tooltips=[
    ("Title", "@HR Employee Name"),
    ("Year", "@Year"),
    ("$", "@Salary")
])

p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tools=[hover])
p.circle(x="x", y="y", source=aspdf)#, size=7, color="color", line_color=None, fill_alpha="alpha")


def select_asp():
    genre_val = genre.value
    director_val = director.value.strip()
    cast_val = cast.value.strip()
    selected = aspdf[
        (aspdf.Reviews >= reviews.value) &
        (aspdf.BoxOffice >= (boxoffice.value * 1e6)) &
        (aspdf.Year >= min_year.value) &
        (aspdf.Year <= max_year.value) &
        (aspdf.Oscars >= oscars.value)
    ]
    if (genre_val != "All"):
        selected = selected[selected.Genre.str.contains(genre_val)==True]
    if (director_val != ""):
        selected = selected[selected.Director.str.contains(director_val)==True]
    if (cast_val != ""):
        selected = selected[selected.Cast.str.contains(cast_val)==True]
    return selected


def update():
    df = select_asp()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d movies selected" % len(df)
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["New Position in Range"],
        title=df["HR Employee Name"],
        year=df["Year"],
        revenue=df["Final Salary FTE"],
        alpha=df["Compa Ratio"],
    )

controls = [reviews, boxoffice, genre, min_year, max_year, oscars, director, cast, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Movies"
