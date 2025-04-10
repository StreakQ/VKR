
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from sqlalchemy.sql import exists
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from repositories import *
from models import Distribution,Theme,AdviserTheme
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment
import os
import subprocess
from werkzeug.security import check_password_hash
from config import ADMIN_PASSWORD_HASH,ADMIN_USERNAME
import json
from decorators import role_required

app = Flask(__name__, template_folder='templates')
app.secret_key = 'key'
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
distribution_repository = DistributionRepository(engine)
student_repository = StudentRepository(engine)
adviser_repository = AdviserRepository(engine)
theme_repository = ThemeRepository(engine)
subject_repository = SubjectRepository(engine)
adviser_theme_repository = AdviserThemeRepository(engine,adviser_repository, theme_repository)
student_theme_interest_repository = StudentThemeInterestRepository(engine,student_repository,theme_repository)
theme_subject_importance_repository = ThemeSubjectImportanceRepository(engine, theme_repository, subject_repository)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/index')
@role_required('admin')
def index():
    with Session() as session:
        distributions = (session.query(Distribution).options(
            joinedload(Distribution.student),
            joinedload(Distribution.adviser),
            joinedload(Distribution.theme)).all()
        )
    return render_template('index.html', distributions=distributions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_form.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with Session() as db_session:
            if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
                session['role'] = 'admin'
                return redirect(url_for('index'))

            student = db_session.query(Student).filter_by(username=username).first()
            if student and check_password_hash(student.password_hash, password):
                session['role'] = 'student'
                session['student_id'] = student.student_id
                return redirect(url_for("form_student"))

        return "Неверный логин или пароль", 401


@app.route('/assign_importances', methods=["GET", "POST"])
@role_required('admin')
def assign_importances():
    if request.method == 'POST':
        try:
            data = request.form
            print(data)
            themes = {}
            for key, value in data.items():
                if key.startswith("theme_name"):
                    theme_index = key.split("_")[-1]
                    themes[theme_index] = {"name": value, "subjects": []}

            # Собираем предметы и веса для каждой темы
            for key, value in data.lists():
                if key.startswith("subject"):
                    theme_index = key.split("_")[1]
                    if theme_index in themes:
                        subjects = value
                        weights = data.getlist(f"weight_{theme_index}")

                        # Связываем предметы и веса
                        for subject_id, weight in zip(subjects, weights):
                            theme_name = themes[theme_index]["name"]
                            theme_subject_importance_repository.add_theme_subject_importance(
                                theme_id=theme_index,
                                subject_id=int(subject_id),
                                weight=float(weight)
                            )
            theme_subject_importance_repository.display_all_theme_subject_importances()
            return "Данные успешно сохранены!", 200

        except Exception as e:
            return f"Произошла ошибка: {e}", 500

    return render_template("assign_importances.html")


@app.route("/assign_advisers_to_themes", methods=["GET", "POST"])
@role_required('admin')
def assign_advisers_to_themes():
    if request.method == 'POST':
        try:
            data = request.form
            print("Полученные данные:", data)

            advisers = {}
            for key, value in data.items():
                if key.startswith("adviser"):
                    adviser_index = key.split("_")[-1]
                    advisers[adviser_index] = {"id": value, "themes": []}

            for key, value in data.lists():
                if key.startswith("theme"):
                    adviser_index = key.split("_")[-1]
                    if adviser_index in advisers:
                        advisers[adviser_index]["themes"].extend(value)

            for adviser_index in advisers:
                adviser_id = advisers[adviser_index]["id"]
                themes = advisers[adviser_index]["themes"]

                # Проверяем существование записей
                record_exists = session.query(
                    exists().where(AdviserTheme.adviser_id == adviser_id)
                ).scalar()

                if record_exists:
                    print(f"Обновление тем для научного руководителя ID {adviser_id}: {themes}")
                    adviser_theme_repository.update_adviser_themes(adviser_id=adviser_id, *themes)
                else:
                    print(f"Добавление тем для научного руководителя ID {adviser_id}: {themes}")
                    adviser_theme_repository.add_adviser_themes(adviser_id=adviser_id, *themes)

            return "Данные успешно сохранены!", 200

        except Exception as e:
            return f"Произошла ошибка: {e}", 500
    return render_template("assign_advisers_to_themes.html")


@app.route("/get_subjects")
@role_required('admin')
def get_subjects():
    try:
        subjects = subject_repository.get_all(Subject)
        list_subjects = [{'id': subject.subject_id, 'name': subject.subject_name} for subject in subjects]
        return jsonify(list_subjects),200
    except Exception as e:
        logging.error(f"Ошибка при получении предметов:{e}")
        return f"Произошла ошибка{e}",500


@app.route("/get_themes", methods=["GET"])
@role_required('admin')
def get_themes():
    try:
        themes = theme_repository.get_all(Theme)
        themes_list = [{"id": theme.theme_id, "name": theme.theme_name} for theme in themes]
        return jsonify(themes_list), 200
    except Exception as e:
        logging.error(f"Ошибка при получении тем: {e}")
        return f"Произошла ошибка: {e}", 500


@app.route("/get_advisers", methods=["GET"])
@role_required('admin')
def get_advisers():
    try:
        advisers = adviser_repository.get_all(Adviser)
        advisers_list = [{"id": adviser.adviser_id, "name": adviser.firstname}for adviser in advisers]
        return jsonify(advisers_list), 200
    except Exception as e:
        logging.error(f"Ошибка при получении научных руководителей")


@app.route("/get_theme_subject_importances", methods=["GET"])
@role_required('admin')
def get_theme_subject_importances():
    try:
        importances = theme_subject_importance_repository.get_all(ThemeSubjectImportance)
        importances_list = [
            {
                "theme_id": importance.theme_id,
                "subject_id": importance.subject_id,
                "weight": round(importance.weight,2)
            }
            for importance in importances
        ]
        return jsonify(importances_list), 200
    except Exception as e:
        logging.error(f"Ошибка при получении связей тем и предметов: {e}")
        return f"Произошла ошибка: {e}", 500


@app.route("/students")
@role_required('admin')
def display_students():
    students = student_repository.get_all(Student)
    return render_template('student_data.html', students=students)


@app.route("/advisers")
@role_required('admin')
def display_advisers():
    advisers = adviser_repository.get_all(Adviser)
    return render_template("adviser_data.html", advisers=advisers)


@app.route("/themes")
@role_required('admin')
def display_themes():
    themes = theme_repository.get_all(Theme)
    return render_template("theme_data.html", themes=themes)


@app.route("/form_student")
def form_student():
    themes = theme_repository.get_all(Theme)
    return render_template("form_student.html",themes=themes)


@app.route("/save_priorities", methods=["POST"])
@role_required('admin')
def save_priorities():
    try:
        priorities_data = request.form.get('priorities')
        if not priorities_data:
            return "Данные не предоставлены", 400

        student_id = session.get('student_id')
        if not student_id:
            return "Студент не авторизован", 401

        priorities = json.loads(priorities_data)
        logging.debug(f"Полученные приоритеты: {priorities}")

        # Обрабатываем каждую пару "тема — приоритет"
        with Session() as db_session:
            # Удаляем все существующие записи для данного студента
            db_session.query(StudentThemeInterest).filter_by(student_id=student_id).delete()
            logging.debug(f"Удалены все записи для Студента ID {student_id}")

            # Добавляем новые записи
            for theme_id, priority in priorities.items():
                theme_id = int(theme_id)
                priority = int(priority)

                new_entry = StudentThemeInterest(
                    student_id=student_id,
                    theme_id=theme_id,
                    interest_level=priority
                )
                db_session.add(new_entry)
                logging.debug(f"Добавлена новая запись: Студент ID {student_id}, Тема ID {theme_id}, Приоритет {priority}")

            db_session.commit()
            student_theme_interest_repository.display_all_student_theme_interests()

        return "Приоритеты успешно сохранены!", 200

    except json.JSONDecodeError:
        return "Некорректные данные JSON", 400
    except Exception as e:
        logging.error(f"Ошибка при сохранении приоритетов: {e}")
        return f"Произошла ошибка: {e}", 500


@app.route("/add_theme", methods=['GET', 'POST'])
@role_required('admin')
def add_theme():
    if request.method == 'POST':
        theme_id = request.form['theme_id']
        theme_name = request.form['theme_name']
        theme_repository.add_theme_for_app(theme_id, theme_name)
        return redirect(url_for('display_themes'))
    return render_template("add_theme.html")


@app.route("/add_adviser", methods=['GET', 'POST'])
@role_required('admin')
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
@role_required('admin')
def add_distribution():
    if request.method == 'POST':
        student_id = request.form['student_id']
        theme_id = request.form['theme_id']
        adviser_id = request.form['adviser_id']
        distribution_repository.add_distribution_for_app(student_id, theme_id, adviser_id)
        return redirect(url_for('index'))

    return render_template('add_distribution.html')


@app.route('/update_distribution/<int:distribution_id>', methods=['GET', 'POST'])
@role_required('admin')
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
@role_required('admin')
def delete_adviser(adviser_id):
    adviser_repository.delete_adviser(adviser_id)
    return redirect(url_for('display_advisers'))


@app.route('/delete_theme/<int:theme_id>', methods=['POST'])
@role_required('admin')
def delete_theme(theme_id):
    theme_repository.delete_theme(theme_id)
    return redirect(url_for('display_themes'))


@app.route('/delete_distribution/<int:distribution_id>', methods=['POST'])
@role_required('admin')
def delete_distribution(distribution_id):
    distribution_repository.delete_distribution(distribution_id)
    return redirect(url_for('index'))


@app.route('/upload_distributions', methods=['GET', 'POST'])
@role_required('admin')
def upload_distributions():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            df = pd.read_excel(file_path)

            for indx, row in df.iterrows():
                student_id = row['student_id']
                theme_id = row['theme_id']
                adviser_id = row['adviser_id']
                distribution_repository.add_distribution_for_app(student_id, theme_id, adviser_id)

            return redirect(url_for('index'))

    return render_template('upload_distributions.html')


@app.route('/upload_themes', methods=['GET', 'POST'])
@role_required('admin')
def upload_themes():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            df = pd.read_excel(file_path)

            for indx, row in df.iterrows():
                theme_name = row['theme_name']
                theme_repository.add_theme(theme_name=theme_name)
            return redirect(url_for('index'))
    return render_template('upload_themes.html')


@app.route('/upload_students', methods=['GET', 'POST'])
@role_required('admin')
def upload_students():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file_path = os.path.join('uploads',file.filename)
            file.save(file_path)
            df = pd.read_excel(file_path)

            for indx, row in df.iterrows():
                student_name = row['student_name']
                group = row['group']
                username = row['username']
                password = row['password']
                student_firstname = student_name.split(" ")[0]
                student_lastname = student_name.split(" ")[1]
                student_patronymic = student_name.split(" ")[2]
                student_repository.add_student(username=username,
                                               password_hash=password,
                                               firstname=student_firstname,
                                               lastname=student_lastname,
                                               patronymic=student_patronymic,
                                               group_student=group)

            return redirect(url_for('index'))
    return render_template('upload_students.html')


@app.route('/upload_advisers', methods=['GET', 'POST'])
@role_required('admin')
def upload_advisers():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file_path = os.path.join('uploads',file.filename)
            file.save(file_path)
            df = pd.read_excel(file_path)

            for indx, row in df.iterrows():
                adviser_name = row['adviser_name']
                username = row['username']
                password = row['password']
                number_of_places = row['number_of_places']
                adviser_firstname = adviser_name.split(" ")[0]
                adviser_lastname = adviser_name.split(" ")[1]
                adviser_patronymic = adviser_name.split(" ")[2]
                adviser_repository.add_adviser(firstname=adviser_firstname,
                                               lastname=adviser_lastname,
                                               patronymic=adviser_patronymic,
                                               number_of_places=number_of_places,
                                               username=username,
                                               password_hash=password)
            return redirect(url_for('index'))
    return render_template('upload_advisers.html')


@app.route('/save_distributions', methods=['GET'])
@role_required('admin')
def save_distributions():
    with Session() as session:
        distributions = (
            session.query(Distribution)
            .options(joinedload(Distribution.student),
                     joinedload(Distribution.theme),
                     joinedload(Distribution.adviser))
            .all()
        )

        if not distributions:
            return redirect(url_for('index'))

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
@role_required('admin')
def unassigned_students():
    unassigned_info = session.get('unassigned_students', None)
    if unassigned_info is None:
        return render_template('unassigned_students.html', unassigned_students=[])
    return render_template("unassigned_students.html", unassigned_students=unassigned_info)


@app.route("/run_main")
@role_required('admin')
def run_main():
    result = subprocess.run([r'C:\PycharmProjects\vkr\.venv\Scripts\python.exe', r'C:\PycharmProjects\vkr\main.py'],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

