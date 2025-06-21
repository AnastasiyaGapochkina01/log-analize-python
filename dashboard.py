from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def dashboard():
    df = pd.read_csv('results.csv', header=None, names=['method', 'status', 'latency'])
    
    plots = {
        'method_pie': create_pie(df, 'method', 'Распределение HTTP методов'),
        'status_pie': create_pie(df, 'status', 'Распределение кодов ответа'),
        'latency_box': create_boxplot(df, 'method', 'latency', 'Время выполнения по методам'),
        'status_latency_scatter': create_scatter(df, 'status', 'latency', 'Зависимость времени от кода ответа')
    }
    
    graphs_html = {name: pio.to_html(fig, full_html=False) for name, fig in plots.items()}
    
    return render_template('dashboard.html', graphs=graphs_html)

def create_pie(df, col, title):
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, 'count']
    return px.pie(counts, names=col, values='count', title=title)

def create_boxplot(df, x_col, y_col, title):
    return px.box(df, x=x_col, y=y_col, title=title, color=x_col)

def create_scatter(df, x_col, y_col, title):
    return px.scatter(df, x=x_col, y=y_col, title=title, color=x_col, opacity=0.7)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
