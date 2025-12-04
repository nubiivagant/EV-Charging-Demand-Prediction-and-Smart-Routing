import matplotlib.pyplot as plt
import seaborn as sns

def plot_clusters(df, k):
    fig, ax = plt.subplots()
    palette = sns.color_palette("bright", k)
    sns.scatterplot(data=df, x='longitude', y='latitude', hue='Cluster', palette=palette, ax=ax)
    for i, row in df.iterrows():
        ax.text(row['longitude'], row['latitude'], row['city'], fontsize=7, alpha=0.6)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(f"EV Stations Clustered into {k} Regions")
    return fig
