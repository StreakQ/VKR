from flask import Flask, render_template, request, redirect, url_for

from models import Distribution
from repositories import DistributionRepository

app = Flask(__name__)
distribution_repository = DistributionRepository()

@app.route('/')
def index():
    distributions = distribution_repository.get_all(DistributionRepository)  
    return render_template('templates/index.html', distributions=distributions)

@app.route('/add_distribution', methods=['GET', 'POST'])
def add_distribution():
    if request.method == 'POST':
        # Получите данные из формы
        student_id = request.form['student_id']
        theme_id = request.form['theme_id']
        adviser_id = request.form['adviser_id']
        interest_level = request.form['interest_level']

        # Добавьте распределение
        distribution_repository.add_distribution(student_id, theme_id, adviser_id, interest_level)
        return redirect(url_for('index'))

    return render_template('templates/add_distribution.html')

@app.route('/update_distribution/<int:distribution_id>', methods=['GET', 'POST'])
def update_distribution(distribution_id):
    distribution = distribution_repository.get_by_id(Distribution,id_field=distribution_id)

    if request.method == 'POST':
        # Получите данные из формы
        student_id = request.form['student_id']
        theme_id = request.form['theme_id']
        adviser_id = request.form['adviser_id']
        interest_level = request.form['interest_level']

        # Обновите распределение
        distribution_repository.update_distribution(distribution_id, student_id, theme_id, adviser_id, interest_level)
        return redirect(url_for('index'))

    return render_template('templates/update_distribution.html', distribution=distribution)

if __name__ == '__main__':
    app.run(debug=True)