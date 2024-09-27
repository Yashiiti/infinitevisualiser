import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Function to generate visualizations
def generate_visualizations(df):
    visualizations = []
    mappings = {}  # To store mappings for categorical columns
    
    # Identify categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Convert categorical columns to numeric with mappings
    for col in categorical_cols:
        unique_values = df[col].unique()
        mappings[col] = {val: idx for idx, val in enumerate(unique_values)}  # Create mapping
        df[col] = df[col].map(mappings[col]).fillna(0).astype(int)  # Convert and fill NaN with 0
    # # Convert any columns that can be converted to numeric
    df_numeric = df.apply(pd.to_numeric, errors='coerce')



    # 1. Correlation heatmap (only for numeric columns)
    if df_numeric.select_dtypes(include='number').shape[1] > 1:
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
    # 3. Scatter plot for pairs of numeric columns
    num_cols = df_numeric.select_dtypes(include='number').columns
    if len(num_cols) >= 2:
        for i in range(len(num_cols)):
            for j in range(i + 1, len(num_cols)):
                fig = px.scatter(df_numeric, x=num_cols[i], y=num_cols[j],
                                title=f'Scatter Plot: {num_cols[i]} vs {num_cols[j]}')
                visualizations.append(fig.to_html())

    num_cols = df_numeric.select_dtypes(include='number').columns
    # if len(num_cols) >= 2:
    #     fig = px.scatter_matrix(df_numeric[num_cols].dropna())
    #     visualizations.append(fig.to_html())

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    df = pd.read_csv(file)
    
    # Generate visualizations
    visualizations = generate_visualizations(df)
    
    return jsonify({'visualizations': visualizations})

if __name__ == '__main__':
    app.run(debug=True)
