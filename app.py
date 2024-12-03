from sqlalchemy.orm import sessionmaker, joinedload
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from repositories import *
from models import Distribution
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment
import os

app = Flask(__name__)

# Создание движка и сессии
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
distribution_repository = DistributionRepository(engine)
student_repository = StudentRepository(engine)
adviser_repository = AdviserRepository(engine)
theme_repository = ThemeRepository(engine)

@app.route('/')
def index():
    session = Session()
    distributions = (session.query(Distribution).options(
        joinedload(Distribution.student),
        joinedload(Distribution.adviser),
    joinedload(Distribution.theme)).all()
    )

    return render_template('index.html', distributions=distributions)

@app.route("/students")
def display_students():
    students = student_repository.get_all(Student)
    return render_template('student_data.html',students=students)

@app.route("/advisers")
def display_advisers():
    advisers = adviser_repository.get_all(Adviser)
    return render_template("adviser_data.html",advisers=advisers)

@app.route("/themes")
def display_themes():
    themes = theme_repository.get_all(Theme)
    return render_template("theme_data.html",themes=themes)
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

@app.route('/delete_distribution/<int:distribution_id>', methods=['POST'])
def delete_distribution(distribution_id):
    distribution_repository.delete_distribution(distribution_id)
    return redirect(url_for('index'))

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

@app.route('/save', methods=['GET'])
def save():
    # Создание новой сессии
    session = Session()

    try:
        # Предварительная загрузка связанных объектов
        distributions = (
            session.query(Distribution)
            .options(joinedload(Distribution.student),
                     joinedload(Distribution.theme),
                     joinedload(Distribution.adviser))
            .all()
        )

        data = {
            'distribution_id': [d.distribution_id for d in distributions],
            'student_name': [f"{d.student.lastname} {d.student.firstname} {d.student.patronymic} " for d in distributions],
            'theme_name': [d.theme.theme_name for d in distributions],
            'adviser_name': [f"{d.adviser.firstname} {d.adviser.lastname}  {d.adviser.patronymic} " for d in distributions]
        }

        # Создание DataFrame
        df = pd.DataFrame(data)

        # Создание нового Excel файла
        wb = Workbook()
        ws = wb.active

        # Заполнение данных в Excel
        for r_idx, row in df.iterrows():
            for c_idx, value in enumerate(row):
                cell = ws.cell(row=r_idx + 1, column=c_idx + 1, value=value)
                # Установка выравнивания по центру
                cell.alignment = Alignment(horizontal='left', vertical='center')

        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width
        # Сохранение файла
        wb.save('distributions.xlsx')
    finally:
        session.close()  # Закрытие сессии

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)