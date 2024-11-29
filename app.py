from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from repositories import DistributionRepository
from models import Distribution
import pandas as pd
import os

app = Flask(__name__)

engine = create_engine('sqlite:///database.db')
distribution_repository = DistributionRepository(engine)

@app.route('/')
def index():
    distributions = distribution_repository.get_all(Distribution)
    return render_template('index.html', distributions=distributions)

@app.route('/add_distribution', methods=['GET', 'POST'])
def add_distribution():
    if request.method == 'POST':
        student_id = request.form['student_id']
        theme_id = request.form['theme_id']
        adviser_id = request.form['adviser_id']
        distribution_repository.add_distribution_for_app(student_id, theme_id, adviser_id)
        return redirect(url_for('index'))

    return render_template('add_distribution.html')

@app.route('/update_distribution/<int:distribution_id>', methods=['GET', 'POST'])
def update_distribution(distribution_id):
    distribution = distribution_repository.get_by_id(Distribution, distribution_id, id_field="distribution_id")

    if request.method == 'POST':
        student_id = request.form['student_id']
        theme_id = request.form['theme_id']
        adviser_id = request.form['adviser_id']
        distribution_repository.update_distribution(distribution_id, student_id, theme_id, adviser_id)
        return redirect(url_for('index'))

    return render_template('update_distribution.html', distribution=distribution)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                student_id = row['student_id']
                theme_id = row['theme_id']
                adviser_id = row['adviser_id']
                distribution_repository.add_distribution_for_app(student_id, theme_id, adviser_id)

            return redirect(url_for('index'))

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)