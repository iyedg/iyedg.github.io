---
title: "Opening up the Tunisian Institute of Statistics' poverty report of 2020"
date: 2020-11-14T21:25:46+01:00
draft: false
toc: true
---

As is the case with most publication from Tunisian public institutions that generate data, the **National Institute of Statistics** (NIS) has recently released a [report on poverty](www.ins.tn%2Fsites%2Fdefault%2Ffiles%2Fpublication%2Fpdf%2FCarte%20de%20la%20pauvret%C3%A9%20en%20Tunisie_final.pdf) in Tunisia as a ... PDF file. The Tunisian citizen in me cringed, the data nerd decided it would make a good project to showcase how to transform a PDF into a more open format, and even throw in some interactive data visualization.

Before moving further in this blog post, it is important to establish what it does, and what it does not.

**What this is not**
  * An analysis of the poverty data in Tunisia, although I am very tempted to do it.
  * A bashing of the **NIS**, they are probably overworked, paid too little, and lack the necessary training to operate and maintain an open data pipeline.

**What this is**
  * A make-up routine for a PDF file using Python, Tabula, Plotly and Streamlit.

If you want to play with the data file you can find it in this [link](https://raw.githubusercontent.com/iyedg/poverty_rate_dashboard/develop/data/processed/poverty_rate_Tunisia_2020.csv). The interactive dashboard is viewable in this [link](https://share.streamlit.io/iyedg/poverty_rate_dashboard/develop/poverty_rate_dashboard/main.py)


## Data extraction from PDF.

The first step of this project is evidently transforming the data inside the PDF into structured data. For this purpose, we will use two excellent Python libraries: Tabula for PDF tables' manipulation, and Pandas for data cleaning and reshaping.


```python {linenos=table}
import tabula
raw_df = tabula.read_pdf("NIS_poverty_report.pdf",
                          pages=40,
                          multiple_tables=True,
                          pandas_options={"header": None})[0]
```

In this snippet, we are telling Tabula to read the file `NIS_poverty_report.pdf`, on page `40` specifically, which has `multiple_tables`. Note that the parameter `multiple_tables` implies that Tabula will return a list of pandas Data Frames, which is why we use the first value in the return value of the `read_pdf` function call. This will become relevant when extracting the data for **Mednine** and **Tataouine** which happen to be on the same page.

A nice tutorial about table extraction from PDF using Table can be found in this [link](https://aegis4048.github.io/parse-pdf-files-while-retaining-structure-with-tabula-py)

```python {linenos=table}
# Will extract the first table identified on page 82

mednine_df = tabula.read_pdf("NIS_poverty_report.pdf",
                          pages=82,
                          multiple_tables=True,
                          pandas_options={"header": None})[0]

# Will extract the second table identified on page 82

tataouine_df = tabula.read_pdf("NIS_poverty_report.pdf",
                          pages=82,
                          multiple_tables=True,
                          pandas_options={"header": None})[1]
```

The other important argument to pay attention to with tabula is `pandas_options`. To properly understand what it does, we simply need to think of the dictionary passed to it as the python convention for passing key word arguments in `**kwargs`. Essentially, after reading the table from PDF, tabula will read the result as a CSV using pandas according to the key word arguments passed in `pandas_options`.

What remains now is to go through the pages specific to each governorate, extract their corresponding table, then merge them into the final dataset. The following snippet provides an overview of the process in code. the full code is available [here](https://github.com/iyedg/poverty_rate_dashboard/blob/develop/poverty_rate_dashboard/process_raw_pdf.py))

```python {linenos=table}
def process_raw_pdf():
    governorates_pages = {
        "Tunis": 40,
        "Ariana": 42,
        "Ben Arous": 44,
        "Manouba": 45,
        "Nabeul": 49,
        "Zagouan": 50,
        "Bizerte": 52,
        "Beja": 55,
        "Jandouba": 56,
        "Kef": 58,
        "Seliana": 62,
        "Sousse": 66,
        "Monastir": 68,
        "Mahdia": 69,
        "Sfax": 71,
        "Kairouan": 73,
        "Kasserine": 75,
        "Sidi Bouzid": 76,
        "Gabes": 79,
        "Médnine": 82,
        "Tataouine": 82,
        "Gafsa": 85,
        "Tozeur": 86,
        "Kebili": 87,
    }

    governorates_dfs = []

    for governorate_name, page in governorates_pages.items():
        if governorate_name == "Tataouine":
            table_index = 1
        else:
            table_index = 0
        df = (
            tabula.read_pdf(
                input_pdf_path,
                pages=page,
                multiple_tables=True,
                pandas_options={"header": None},
            )[table_index]
            .pipe(cleaning_pipeline) # Using a pandas pipelines to cleanup individual data frames
            .assign(Gouvernorat=governorate_name)
        )

        governorates_dfs.append(df)
    combined_df = pd.concat(governorates_dfs, ignore_index=True)
    combined_df.to_csv(
        here("data/processed/poverty_rate_Tunisia_2020.csv"), index=False
    )
    return combined_df
```

## Agumenting the data: fuzzy string matching

The dataset we have extracted thus far can be visualized as is to get insights about regional differences in poverty rates, and how that can be related to primary and secondary schools abandonment rates. That is all good and well, but I wanted a map (the technical term is a Choropleth map, from the Greek *Choros* for area and *Plethos* for multitude).

As such, I have embarked on the journey to augment the dataset with the administrative borders of Tunisian delegations. Getting the data was relatively simple, the kind people at [data4tunisia](https://www.data4tunisia.org) host a platform where a variety of entities and people can share their data publically, which is [where](https://www.data4tunisia.org/en/datasets/decoupage-de-la-tunisie-geojson-et-shapefile/#_) I got the geo data for Tunisian delegations.

The challenge that jumps at us right away is that the key variables used to join the datasets i.e. the governorate name and the delegation name are not written the same way. To better illustrate the problem, let us look at a subset of the municipality names we are trying to match.

| Delegation name form NIS   | Delegation name from Geo data   |
|:---------------------------|:--------------------------------|
| Ettahrir                   | El Tahrir                       |
| Tina                       | Thyna                           |
| La Medina                  | Médina                          |
| Ariana Ville               | Ariana Médina                   |
| Souk Lahad                 | Souk El Ahed                    |
| Elksar                     | Ksar                            |
| Boumhel Bassatine          | Boumhel                         |
| Sidi Ali Ben Nasrallah     | Nasrallah                       |
| Sfax Ville                 | Sfax Médina                     |
| Sidi Amor Bou Hajla        | Bouhajla                        |


With 264 unique delegation names *(there are 264 delegations but two of them are called **Ezzouhour**)*, this task has to be done programatically. The best way I found to deal with this is by formulating the challenge as an [**Assignment problem**](https://en.wikipedia.org/wiki/Assignment_problem). In essence, this entails building a cost matrix between the names from the NIS and the names from the Geo data where the cost is some measure of distance between the text of the two names, then running an optimization algorithm that will assign matching names such as to minimize the total distance *(or cost)* between the matched names.

For the implementation of this step we resort to two excellent python packages: [TextDistance](https://github.com/life4/textdistance) and [SciPy](https://github.com/scipy/scipy). With TextDistance we have access to a wide variety of text distance metrics, but I have settled through experimentation on the [Jaccard Index](https://en.wikipedia.org/wiki/Jaccard_index). As for the optimization algorithm we will use the [Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm).

```python {linenos='table'}
NSI_names = [
    "Ettahrir",
    "Tina",
    "La Medina",
    "Ariana Ville",
    "Souk Lahad",
    "Elksar",
    "Boumhel Bassatine",
    "Sidi Ali Ben Nasrallah",
    "Sfax Ville",
    "Sidi Amor Bou Hajla",
]
geodata_names = [
    "El Tahrir",
    "Thyna",
    "Médina",
    "Ariana Médina",
    "Souk El Ahed",
    "Ksar",
    "Boumhel",
    "Nasrallah",
    "Sfax Médina",
    "Bouhajla",
]

# We shuffle them randomly to avoid having the existing order affecting the algorithm
# even though theoretically it does not matter
shuffle(NSI_names)
shuffle(geodata_names)
```

Now we compute the cost matrix as follows:

```python

pairs = product(NSI_names, geodata_names)

scores = np.array(
    [textdistance.jaccard.normalized_distance(q, c) for q, c in pairs]
).reshape((len(NSI_names), len(geodata_names)))
```


|                        |   Boumhel |   Bouhajla |   Souk El Ahed |    Thyna |   Médina |   Nasrallah |   Sfax Médina |     Ksar |   El Tahrir |   Ariana Médina |
|:-----------------------|----------:|-----------:|---------------:|---------:|---------:|------------:|--------------:|---------:|------------:|----------------:|
| Souk Lahad             |  0.785714 |   0.615385 |       0.533333 | 0.846154 | 0.857143 |    0.8125   |      0.6875   | 0.923077 |    0.8125   |        0.789474 |
| Ariana Ville           |  0.882353 |   0.823529 |       0.8      | 0.866667 | 0.8      |    0.6875   |      0.722222 | 0.857143 |    0.6875   |        0.529412 |
| Tina                   |  1        |   0.909091 |       1        | 0.5      | 0.571429 |    0.916667 |      0.75     | 0.857143 |    0.7      |        0.785714 |
| Sidi Ali Ben Nasrallah |  0.84     |   0.8      |       0.692308 | 0.875    | 0.833333 |    0.590909 |      0.730769 | 0.869565 |    0.76     |        0.6      |
| Elksar                 |  0.916667 |   0.833333 |       0.8      | 0.9      | 0.909091 |    0.636364 |      0.9375   | 0.571429 |    0.636364 |        0.882353 |
| Boumhel Bassatine      |  0.588235 |   0.611111 |       0.73913  | 0.842105 | 0.85     |    0.761905 |      0.782609 | 0.894737 |    0.761905 |        0.8      |
| La Medina              |  0.933333 |   0.866667 |       0.833333 | 0.833333 | 0.5      |    0.875    |      0.461538 | 0.916667 |    0.8      |        0.533333 |
| Sidi Amor Bou Hajla    |  0.761905 |   0.65     |       0.652174 | 0.956522 | 0.863636 |    0.833333 |      0.75     | 0.904762 |    0.782609 |        0.666667 |
| Sfax Ville             |  0.866667 |   0.875    |       0.777778 | 0.928571 | 0.857143 |    0.8125   |      0.6      | 0.923077 |    0.733333 |        0.85     |
| Ettahrir               |  0.928571 |   0.857143 |       0.888889 | 0.818182 | 0.833333 |    0.785714 |      0.882353 | 0.8      |    0.454545 |        0.833333 |


For the actual optimization, we call the `linear_sum_assignment` from the module `scipy.optimize` which applies the Hungarian algorithm to our cost matrix.

```python
row_ind, col_ind = linear_sum_assignment(scores)

scores_df = pd.DataFrame(
    [
        {"source": NSI_names[i], "target": geodata_names[j], "distance": scores[i, j]}
        for i, j in zip(row_ind, col_ind)
    ]
).sort_values("distance")
```

Which gives the correct assignments

| source                 | target        |   distance |
|:-----------------------|:--------------|-----------:|
| Ettahrir               | El Tahrir     |   0.454545 |
| Tina                   | Thyna         |   0.5      |
| La Medina              | Médina        |   0.5      |
| Ariana Ville           | Ariana Médina |   0.529412 |
| Souk Lahad             | Souk El Ahed  |   0.533333 |
| Elksar                 | Ksar          |   0.571429 |
| Boumhel Bassatine      | Boumhel       |   0.588235 |
| Sidi Ali Ben Nasrallah | Nasrallah     |   0.590909 |
| Sfax Ville             | Sfax Médina   |   0.6      |
| Sidi Amor Bou Hajla    | Bouhajla      |   0.65     |


## Parting words

This project was truly fun because the actual data collection was not hard but it had enough challenges to keep it interesting. For such a basic project I dealt with extracting data from PDFs, Fuzzy string matching, Optimization algorithms and the final step which is turning the results into an interactive dashboard which you can find [here](https://share.streamlit.io/iyedg/poverty_rate_dashboard/develop/poverty_rate_dashboard/main.py).


<video autoplay loop style="width:100%;">
        <source src="videos/dashboard.webm" type="video/webm">
</video>

For the full code used in this project please visit my Github [repo](https://github.com/iyedg/poverty_rate_dashboard/)

