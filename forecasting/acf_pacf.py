import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def plot_acf_pacf(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    plot_acf(df, ax=axes[0])
    plot_pacf(df, ax=axes[1])
    plt.savefig("static/acf_pacf.png")
    return "static/acf_pacf.png"
