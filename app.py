from sqlalchemy.orm import sessionmaker, joinedload
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from repositories import *
from models import Distribution
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment
import os
import subprocess
from main import check_unassigned_students,main

app = Flask(__name__)
app.secret_key = 'key'
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
distribution_repository = DistributionRepository(engine)
student_repository = StudentRepository(engine)
adviser_repository = AdviserRepository(engine)
theme_repository = ThemeRepository(engine)

@app.route('/')
def index():
    with Session() as session:
        distributions = (session.query(Distribution).options(
            joinedload(Distribution.student),
            joinedload(Distribution.adviser),
            joinedload(Distribution.theme)).all()
        )
    return render_template('index.html', distributions=distributions)


@app.route("/run_main")
def run_main():
    result = subprocess.run([r'C:\PycharmProjects\vkr\.venv\Scripts\python.exe', r'C:\PycharmProjects\vkr\main.py'],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)

    # Получаем неназначенных студентов
    unassigned_students_list, student_repository, student_theme_interest_repository, adviser_repository = main()
    unassigned_info = check_unassigned_students(unassigned_students_list, student_repository,
                                                student_theme_interest_repository)

    # Сохраняем неназначенных студентов в сессии
    session['unassigned_students'] = unassigned_info

    return redirect(url_for('index'))

@app.route("/students")
def display_students():
    students = student_repository.get_all(Student)
    return render_template('student_data.html', students=students)

@app.route("/advisers")
def display_advisers():
    advisers = adviser_repository.get_all(Adviser)
    return render_template("adviser_data.html", advisers=advisers)

@app.route("/themes")
def display_themes():
    themes = theme_repository.get_all(Theme)
    return render_template("theme_data.html", themes=themes)

@app.route("/add_theme", methods=['GET' , 'POST'])
def add_theme():
    if request.method == 'POST':
        theme_id = request.form['theme_id']
        theme_name = request.form['theme_name']
        theme_repository.add_theme_for_app(theme_id, theme_name)
        return redirect(url_for('display_themes'))
    return render_template("add_theme.html")

@app.route("/add_adviser", methods=['GET', 'POST'])
def add_adviser():
    if request.method == 'POST':
        adviser_id = request.form['adviser_id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        patronymic = request.form['patronymic']
        number_of_places = request.form['number_of_places']
        adviser_repository.add_adviser_for_app(adviser_id, firstname, lastname, patronymic, number_of_places)
        return redirect(url_for("display_advisers"))
    return render_template("add_adviser.html")

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

@app.route('/delete_adviser/<int:adviser_id>', methods=['POST'])
def delete_adviser(adviser_id):
    adviser_repository.delete_adviser(adviser_id)
    return redirect(url_for('display_advisers'))

@app.route('/delete_theme/<int:theme_id>', methods=['POST'])
def delete_theme(theme_id):
    theme_repository.delete_theme(theme_id)
    return redirect(url_for('display_themes'))

@app.route('/delete_distribution/<int:distribution_id>', methods=['POST'])
def delete_distribution(distribution_id):
    distribution_repository.delete_distribution(distribution_id)
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
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
    with Session() as session:
        distributions = (
            session.query(Distribution)
            .options(joinedload(Distribution.student),
                     joinedload(Distribution.theme),
                     joinedload(Distribution.adviser))
            .all()
        )

        if not distributions:
            return redirect(url_for('index'))  # Если нет данных, перенаправляем

        data = {
            'distribution_id': [d.distribution_id for d in distributions],
            'student_name': [f"{d.student.lastname} {d.student.firstname} {d.student.patronymic}" for d in distributions],
            'theme_name': [d.theme.theme_name for d in distributions],
            'adviser_name': [f"{d.adviser.firstname} {d.adviser.lastname} {d.adviser.patronymic}" for d in distributions]
        }

        df = pd.DataFrame(data)
        wb = Workbook()
        ws = wb.active

        for r_idx, row in df.iterrows():
            for c_idx, value in enumerate(row):
                cell = ws.cell(row=r_idx + 1, column=c_idx + 1, value=value)
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

        wb.save('distributions.xlsx')

    return redirect(url_for('index'))


@app.route('/unassigned_students')
def unassigned_students():
    unassigned_info = session.get('unassigned_students', None)
    if unassigned_info is None:
        return render_template('unassigned_students.html', unassigned_students=[])  # Если нет неназначенных студентов, передаем пустой список
    return render_template('unassigned_students.html', unassigned_students=unassigned_info)



if __name__ == '__main__':
    app.run(debug=True)

# <!--    <a href="{{url_for('choose_interest_themes')}}">Выбор интересующих тем</a>-->
# <!--            <a href="{{ url_for('display_theme_subjects') }}">Таблица связи тем и предметов</a>-->
# <!--            <a href="{{ url_for('display_adviser_themes') }}">Таблица связи научных руководителей и тем</a>-->
# <!--            <a href="{{ url_for('display_student_theme_interests') }}">Таблица интересов студентов</a>-->