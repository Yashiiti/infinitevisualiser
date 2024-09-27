import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io
import base64

def generate_visualizations(df):
    visualizations = []

    # Convert any columns that can be converted to numeric
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    
    # 1. Correlation heatmap (only for numeric columns)
    if df_numeric.select_dtypes(include='number').shape[1] > 1:  # Ensure at least 2 numeric columns
        plt.figure(figsize=(10, 8))
        sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Heatmap')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        visualizations.append(base64.b64encode(buf.getvalue()).decode('utf-8'))
        plt.close()

    # 2. Pair plot (only for numeric columns and limited number of columns)
    if len(df_numeric.columns) <= 10:
        sns.pairplot(df_numeric.dropna())  # Drop rows with NaN values for pairplot
        plt.title('Pair Plot')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        visualizations.append(base64.b64encode(buf.getvalue()).decode('utf-8'))
        plt.close()

    # 3. Scatter plot (if at least 2 numeric columns)
    num_cols = df_numeric.select_dtypes(include='number').columns
    if len(num_cols) >= 2:
        fig = px.scatter_matrix(df_numeric[num_cols].dropna())
        visualizations.append(fig.to_html())

    # 4. Distribution plots for numeric columns
    for col in num_cols:
        sns.histplot(df_numeric[col].dropna(), kde=True)
        plt.title(f'Distribution Plot - {col}')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        visualizations.append(base64.b64encode(buf.getvalue()).decode('utf-8'))
        plt.close()

    return visualizations
df=pd.read_csv('dummy_data.csv')
generate_visualizations(df)