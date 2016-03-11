import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from load_data import load_data
from matplotlib.backends.backend_pdf import PdfPages


def plot_counts():

    df = load_data()
    counts = np.zeros(6)
    for i in range(len(counts)):
        counts[i] = len(pd.unique(df[df.columns[i]].values.ravel())) - 1
    taxo = list(df.columns.values)[:6]
    df_count = pd.DataFrame(counts, taxo)
    df_count.columns = ['UniqueCounts']
    pp = PdfPages('counts_plot.pdf')
    plt.figure()
    plt.clf()
    sns.barplot(x=df_count.index, y=df_count['UniqueCounts'])
    plt.title('Unique groups in our dataset at different taxonomic ranks')
    plt.xlabel('Taxonomic ranks')
    plt.ylabel('Counts')
    pp.savefig()
    pp.close()

# Run the following code if the file is run at the command line


def main():
    return plot_counts()

if __name__ == "__main__":
    main()