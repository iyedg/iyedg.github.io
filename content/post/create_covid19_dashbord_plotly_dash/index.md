---
title: "Get started with Plotly Dash: a COVID19 dashboard for Tunisia"
date: 2020-05-02T10:33:25+01:00
draft: false
tags: ["plotly", "python", "dashboards"]
---

Can you create a pretty and usable dashboard without knowing much about frontend development ?
Various attempts at making the answer to this question a `YES` have been made with varying degrees of success.
Probably the most famous attempts are tools like PowerBI Microsoft or Tableau which have a relatively low barrier to entry compared to solutions that involve coding.
Even the omnipresent *(but far form omnipotent)* Excel could be used as a dashboarding tool.
But that comes at a cost of lower customizability / extensibility.
It goes without saying that using these solutions for commercial uses
 cost vastly more despite having very usable versions for users who wish 
 to try the tools.

In this tutorial we will focus on [**Dash**](https://dash.plotly.com/) by Plotly,
the creators of the [eponymous plotting library](https://github.com/plotly/plotly.py).
Keep in mind, however, that the python ecosystem offers a variety of tools with various tradeoffs and considerations.
None of these solutions is a cure-all, therefore it is wise to keep an open mind and tinker with some of them *(all of them ?)*.

* [**Streamlit**](https://www.streamlit.io/), [(gallery)](https://www.streamlit.io/gallery)
* [**Voilà**](https://github.com/voila-dashboards/voila), [(gallery)](https://voila-gallery.org/)
* [**Panel**](https://panel.holoviz.org/index.html), [(gallery)](https://panel.holoviz.org/index.html)
* Or go full [NIH](https://en.wikipedia.org/wiki/Not_invented_here) and build your own with [**Flask**](https://flask.palletsprojects.com/en/1.1.x/)


By the end of this tutorial we will have a dashboard that looks like this:

<figure>
<video controls style="width:100%" src="videos/another.mkv"></video>
<figcaption>
<span>End result</span>
</figcaption>
</figure>

## Elements of a `Plotly Dash` project

It is important before we start building our dashboard that we understand some concepts driving **Dash**.
The first idea we will touch on is *reactive programming*.

### Reactivity and Callbacks

Even if you don't know what *reactive programming* means you've most likely used it in ... Excel.

In Excel, when we use a formula to compute the sum of two cells,
as soon as a value in the summation changes, the formula cell recomputes its value in reaction.

<figure>
<video controls style="width:100%" src="videos/excel_reactive.mkv" id="excel_reactive"></video>
<figcaption>
<span>Excel is a reactive program</span>
</figcaption>
</figure>


The equivalent idea to an Excel formula for Dash is a callback function.

```python {linenos=table,hl_lines=["1-4"]}
@app.callback(
    output=Output("ouput-cell", "value"),
    inputs=[Input("cell-1", "value"), Input("cell-2", "value")],
)
def sum_of_cell1_and_cell2(value_of_cell1, value_of_cell2):
    return value_of_cell1 + value_of_cell2
```

In the highlighted lines 1-4, we are saying that the attribute `value` of an object with and ID of `output-cell` should react to
changes in the `value` attribute of the objects with ID `cell-1` and `cell-2`.

```python {linenos=table,hl_lines=["5-6"]}
@app.callback(
    output=Output("ouput-cell", "value"),
    inputs=[Input("cell-1", "value"), Input("cell-2", "value")],
)
def sum_of_cell1_and_cell2(value_of_cell1, value_of_cell2):
    return value_of_cell1 + value_of_cell2
```


<figure>
<image src="images/reactivity_callback_chain.png">
<figcaption>
<span>Callbacks diagram</span>
</figcaption>
</figure>


In the function definition we describe how the `value` attribute of `output-cell` should react
to a change in the `value` attribute of `cell-1` and / or `cell-2`.
In our case that would be to return the sum of the values.

It is not important to focus on the syntax for now,
we are simply building a conceptual model of how Dash works.
One question that arises from the snippet we have just seen is *what are* `output-cell`, `cell-1` *and* `cell-2` *?*

### Layout

To continue our Excel simile, let us think of an Excel cell as a special kind of user interface components.
In essence, a cell in a spredsheet is not that much different from an input box, a checkbox, or a dropdown list.
These user interface elements can hold various attributes of their own, including a `value` attribute,
and allow the user to trigger callbacks which ultimately allows our dashboard to *react* to user input.

```python {linenos=table,hl_lines=["8-14"]}
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        dcc.Input(id="cell-1", type="number", value=30),
        dcc.Input(id="cell-2", type="number", value=4),
        html.H1(id="output-cell"),
    ]
)

@app.callback(
    output=Output("output-cell", "children"),
    inputs=[Input("cell-1", "value"), Input("cell-2", "value")],
)
def sum_of_cell1_and_cell2(value_of_cell1, value_of_cell2):
    return int(value_of_cell1) + int(value_of_cell2)

if __name__ == "__main__":
    app.run_server(host="localhost", debug=True)
```

With the addition of a layout as described in the lines 8 through 14, our dashboard can now
display a user interface, and react to changes triggered by user input. Running the code above results in
the following "*dashboard*"

<figure>
<video controls src="videos/excel_dash.mkv" style="width: 100%" id="excel_dash"></video>
<figcaption>
<span>First Dash dashboard</span>
</figcaption>
</figure>


## Getting our hands dirty

<figure>
<video autoplay loop src="videos/ghost_in_the_shell.mp4" style="width: 100%"></video>
<figcaption>
<span>Ghost in the Shell (1995)</span>
</figcaption>
</figure>


### Virtual environment and dependencies installation

### Directory structure

For this project we will need to install the following dependencies:

* **dash** is the library that will provide two components for our project: the dashboarding and the plotting through `plotly-express` which we will introduce as we go.
* **dash-bootstrap-components** will allow us to theme our app using Bootstrap which provides useful layout capabilities and interesting components. For this tutorial we will limit ourselves to using the Grid
* **pandas** which we will use for the data manipulation part.
* **geopandas** will be of use when plotting data on a map.
* **pyprojroot** is a small utility library that allows us to reference files inside our project using paths relative the root of our project instead of absolute *long* paths.

You can install them using the following command

```bash
pip install dash==1.11.0 dash-bootstrap-components pandas geopandas requests pyprojroot
```

The directory structure that we will need looks as follows

```bash
.
├── data
│  └── raw
└── src
   ├── __init__.py
   ├── app.py
   ├── callbacks.py
   ├── cli.py
   ├── data.py
   ├── index.py
   ├── layouts.py
   └── plots.py
```

To create it you can run the following commands

```sh
md -p plotly_dash_tutorial/{data/raw,src}
cd plotly_dash_tutorial
touch src/__init__.py # Making a python package named src
touch src/{app.py,index.py} # General application / dashboard code
touch src/{callbacks.py,layouts.py} # Plotly dash specific code
touch src/{plots.py,data.py} # The model part of our application
```

### Application setup

To setup our app, we need to create an `app` object.
This object is central to our application in the sense that it acts as the
orchestrator of the interaction between our layout components through the callbacks we define.

**app.py**

```python {linenos=table}
import dash

import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI, "custom.css"])
```
**index.py**

```python {linenos=table,hl_lines=["1-5"]}
import callbacks
from app import app
from layouts import layout

app.layout = layout

if __name__ == "__main__":
    app.run_server(host="localhost", debug=True)
```

In the highlighted lines in the snippet above, we allow the interaction between
the three main components of our app to happen: *`app` object*, *layouts* and
*callbacks*.

### Creating the base layout

**layouts.py**

```python {linenos=table}
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .data import by_gov_indicators, geo_targa_covid_df, last_update
from .plots import plot_part_of_daily_active_cases
```

Let's begin by discussing the imported modules for `layouts.py`.
`dash_bootstrap_components`, `dash_core_components` and `dash_html_components`
contain components which correspond to HTML elements. These are what largely
liberates the developers from actually writing HTML, CSS which are responsible
for the View layer of our dashboard. The components provided by these modules
can vary in complexity from being a mere text container such as `html.H1` to a
full interactive table such as `dcc.DataTable`. It is generally useful to keep
the documentation from theses modules open in a side tab while creating the
dashboard.

The general layout of our page is composed of two major containers, a sidebar
and a main content area.

**layouts.py**

```python {linenos=table,linenostart=26}
sidebar = html.Div(
    [
        html.H3("COVID19 dashboard for cases in Tunisia"),
        html.Hr(),
        dcc.Dropdown(id="dropdown_criteria"),
    ],
    style=SIDEBAR_STYLE,
)
```

The snippet above uses components from `dash_html_components` and
`dash_core_components`. As a rule of thumb, components from
`dash_html_components` correspond to HTML elements, and they are named as such.
For instance, an `h1` element in raw HTML corresponds to `html.H1` *(notice the
capitalization)*. By contrast, components from `dash_core_components` contain
components with interactivity baked into them such as tabs, dropdown lists and
data tables.

**layouts.py**

```python {linenos=table,linenostart=36}
main_container = dbc.Container(
    [
        dcc.Graph(
            figure=px.scatter(
                pd.DataFrame(random_df_data),
                x=0,
                y=1,
                template="plotly_white",
                title="My chart title",
            )
        )
    ],
    style=MAIN_CONTAINER_STLE,
    id="main_container",
)
```
Our main container uses the `bcc.Container` component whose' name is
self-descriptive. It is however important that we understand that this component
and similar *layout* components, do not translate directly into visible elements
on our page, instead they modify the *position* of elements on the page. In
addition, the `Container` component comes with the added benefit of adding
*responsivity* to our page thanks to being based on Bootstrap, which further
improves the usability of our dashboard.

To create the scatter plot visible in the main content area, we use a
`dcc.Graph` component in tandem with a `plotly_express` chart. Keep in mind
however that the `dcc.Graph` component takes any figure object that corresponds
to plotly.js schema, be it created through `plotly_express`, the
`plotly.graph_objects` or even manually as nested python dictionaries.

**layouts.py**
```python {linenos=table,linenostart=36,hl_lines=["3-11"]}
main_container = dbc.Container(
    [
        dcc.Graph(
            figure=px.scatter(
                pd.DataFrame(random_df_data),
                x=0,
                y=1,
                template="plotly_white",
                title="My chart title",
            )
        )
    ],
    style=MAIN_CONTAINER_STLE,
    id="main_container",
)
```


It is also worth noting that we must assign and `id` to each component we will
interact with later on in our callbacks.

```python {linenos=table,linenostart=49}
id="main_container"
```



## Further reading

* [Official documentation on multi-page apps](https://dash.plotly.com/urls)
* https://medium.com/@mbostock/a-better-way-to-code-2b1d2876a3a0
* https://pbpython.com/plotly-dash-intro.html
* https://www.statworx.com/de/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/#contents
* https://aatishb.com/covidtrends/