# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # EDA

# +
import pandas as pd
import plotly.express as px
from pyprojroot import here
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()
# -

engine = create_engine(
    URL(drivername="sqlite", database=str(here("data/municipal_performance.sqlite3")))
)
Base.prepare(engine, reflect=True)

Municipality = Base.classes.municipalities
Governorate = Base.classes.governorates
Evaluation = Base.classes.evaluations
Criterion = Base.classes.criteria

session = Session(engine)

q = (
    session.query(
        Municipality.name_fr, Evaluation.score, Criterion.max_score, Criterion.name_fr
    )
    .filter(Evaluation.year == 2018)
    .filter(Criterion.level == "domain")
    .join(Municipality)
    .join(Criterion)
)

plot_df = (
    pd.DataFrame(
        data=q.all(),
        columns=[
            "municipality_name_fr",
            "evaluation_score",
            "criterion_max_score",
            "evaluation_criterion",
        ],
    )
    .pipe(
        lambda df: df.assign(
            evaluation_score=100 * df["evaluation_score"].div(df["criterion_max_score"])
        )
    )
    .drop(columns=["criterion_max_score"])
    .pivot_table(
        index=["municipality_name_fr"],
        columns=["evaluation_criterion"],
        values=["evaluation_criterion"],
        aggfunc="sum",
    )
    .pipe(lambda df: df.set_axis(df.columns.get_level_values(1), axis="columns"))
    .pipe(lambda df: df.assign(Score=df.sum(axis=1).div(3)))
    .reset_index()
)
plot_df

fig_3D = px.scatter_3d(
    plot_df,
    x=plot_df.columns[1],
    y=plot_df.columns[2],
    z=plot_df.columns[3],
    hover_data=plot_df.columns,
    color="Score",
    template="plotly_white",
    color_continuous_scale=px.colors.sequential.Viridis,
)
fig_3D

fig_a = px.scatter_ternary(
    plot_df,
    a=plot_df.columns[1],
    b=plot_df.columns[2],
    c=plot_df.columns[3],
    hover_data=plot_df.columns,
    color="Score",
    template="plotly_white",
    color_continuous_scale=px.colors.sequential.Viridis,
)
fig_a.update_traces(marker=dict(symbol="x"))

# +
import itertools

n = 3
fig_b = (
    pd.DataFrame(
        list(
            map(
                lambda x: dict(zip(["a", "b", "c"], x)),
                itertools.product([0, 1], repeat=n),
            )
        )
    )
    .assign(size=10)
    .pipe(
        lambda df: px.scatter_ternary(
            df, "a", "b", "c", size="size", template="plotly_white"
        )
    )
)
# -

from plotly.subplots import make_subplots

fig = make_subplots(
    cols=3,
    specs=[[{"type": "scatterternary"}, {"type": "scatterternary"}, {"type": "scene"}]],
)

fig.add_trace(fig_b.data[0], row=1, col=1)
fig.add_trace(fig_a.data[0], row=1, col=2)
fig.add_trace(fig_3D.data[0], row=1, col=3)
fig.update_layout(template="plotly_white")

# ## t-SNE

q = (
    session.query(
        Municipality.name_fr, Evaluation.score, Criterion.max_score, Criterion.name_fr
    )
    .filter(Evaluation.year == 2018)
    .filter(Criterion.level == "criterion")
    .join(Municipality)
    .join(Criterion)
)
print(q)

hd_data_df = pd.DataFrame(
    data=q.all(),
    columns=[
        "municipality_name_fr",
        "evaluation_score",
        "criterion_max_score",
        "evaluation_criterion",
    ],
).pivot_table(
    index=["municipality_name_fr"],
    columns=["evaluation_criterion"],
    values=["evaluation_score"],
)

from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering, KMeans, SpectralClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(hd_data_df)

pca = PCA(n_components="mle")
pca.fit(X_scaled)
pca_df = pd.DataFrame(
    pca.transform(X_scaled), columns=[f"PC{i}" for i in range(1, pca.n_components_ + 1)]
)

pca_df

pca.explained_variance_ratio_

px.area(y=100 * pca.explained_variance_ratio_.cumsum(), template="plotly_white")

varimax_pca = FactorAnalyzer(n_factors=25, rotation="varimax", method="principal")
varimax_pca.fit(X_scaled)
varimax_pca_df = pd.DataFrame(
    varimax_pca.transform(X_scaled),
    columns=[f"PC{i}" for i in range(1, pca.n_components_ + 1)],
)

calculate_kmo(X_scaled)

calculate_bartlett_sphericity(X_scaled)

_, _, explained_variance_cumsum = varimax_pca.get_factor_variance()
px.area(y=100 * explained_variance_cumsum)

original_eigen_values, common_factor_eigen_values = varimax_pca.get_eigenvalues()

common_factor_eigen_values

spec_clust = SpectralClustering(n_clusters=3)
spec_clust.fit(varimax_pca_df)

agg_clust = AgglomerativeClustering(
    n_clusters=3, compute_full_tree=True, linkage="complete"
)
agg_clust.fit(varimax_pca_df)

kmeans_clust = KMeans(n_clusters=3)
kmeans_clust.fit(varimax_pca_df)

tsne = TSNE(n_components=3)
tsne_results = tsne.fit_transform(varimax_pca_df.iloc[:, :10])

spec_fig = px.scatter_3d(
    x=tsne_results[:, 0],
    y=tsne_results[:, 1],
    z=tsne_results[:, 2],
    color=[str(i) for i in spec_clust.labels_],
    height=700,
    width=700,
)
agg_fig = px.scatter_3d(
    x=tsne_results[:, 0],
    y=tsne_results[:, 1],
    z=tsne_results[:, 2],
    color=[str(i) for i in agg_clust.labels_],
    height=700,
    width=700,
)
kmeans_fig = px.scatter_3d(
    x=tsne_results[:, 0],
    y=tsne_results[:, 1],
    z=tsne_results[:, 2],
    color=[str(i) for i in kmeans_clust.labels_],
    height=700,
    width=700,
)

fig = make_subplots(
    cols=3,
    shared_xaxes="all",
    shared_yaxes="all",
    subplot_titles=["Spectral", "Agglomerative", "K-Means"],
    specs=[[{"type": "scene"}, {"type": "scene"}, {"type": "scene"}]],
)
fig.add_traces(spec_fig.data, cols=1, rows=1)
fig.add_traces(agg_fig.data, cols=2, rows=1)
fig.add_traces(kmeans_fig.data, cols=3, rows=1)
fig.update_layout(template="plotly_white")

spec_fig_pca = px.scatter(
    x=tsne_results[:, 1],
    y=tsne_results[:, 2],
    color=[str(i) for i in spec_clust.labels_],
    height=700,
    width=700,
)
agg_fig_pca = px.scatter(
    x=tsne_results[:, 1],
    y=tsne_results[:, 2],
    color=[str(i) for i in agg_clust.labels_],
    height=700,
    width=700,
)
kmeans_fig_pca = px.scatter(
    x=tsne_results[:, 1],
    y=tsne_results[:, 2],
    color=[str(i) for i in kmeans_clust.labels_],
    height=700,
    width=700,
)

fig = make_subplots(
    cols=3,
    shared_xaxes=True,
    shared_yaxes=True,
    subplot_titles=["Spectral", "Agglomerative", "K-Means"],
    specs=[[{"type": "scatter"}, {"type": "scatter"}, {"type": "scatter"}]],
)
fig.add_traces(spec_fig_pca.data, cols=1, rows=1)
fig.add_traces(agg_fig_pca.data, cols=2, rows=1)
fig.add_traces(kmeans_fig_pca.data, cols=3, rows=1)
fig.update_layout(template="plotly_white")

# +
labels = agg_clust.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X_scaled, labels))

# +
labels = spec_clust.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X_scaled, labels))
# -


