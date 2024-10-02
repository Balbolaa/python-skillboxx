import datetime
import sqlite3
import random
from typing import Optional

# SQL queries to create the database schema
CREATE_DATABASE_QUERY = """
DROP TABLE IF EXISTS 'teachers';  -- Drop 'teachers' table if it already exists
CREATE TABLE 'teachers' (         -- Create 'teachers' table with a unique ID and full name
    teacher_id integer PRIMARY KEY,
    full_name VARCHAR(20)
);

DROP TABLE IF EXISTS 'students_groups';  -- Drop 'students_groups' if it already exists
CREATE TABLE 'students_groups' (         -- Create 'students_groups' with a unique ID and a foreign key for 'teachers'
    group_id INTEGER PRIMARY KEY,
    teacher_id INTEGER REFERENCES teachers(teacher_id)
);

DROP TABLE IF EXISTS 'students';  -- Drop 'students' table if it already exists
CREATE TABLE 'students' (         -- Create 'students' table with a unique ID, full name, and a foreign key for 'students_groups'
    student_id INTEGER PRIMARY KEY,
    full_name VARCHAR(20),
    group_id INTEGER REFERENCES students_groups(group_id)
);

DROP TABLE IF EXISTS 'assignments';  -- Drop 'assignments' table if it already exists
CREATE TABLE 'assignments' (         -- Create 'assignments' table with a unique ID, foreign keys for 'teachers' and 'students_groups', due date, and assignment text
    assisgnment_id INTEGER PRIMARY KEY,
    teacher_id REFERENCES teachers(teacher_id),
    due_date varchar(255),
    group_id INTEGER REFERENCES students_groups(group_id),
    assignment_text VARCHAR(100)
);

DROP TABLE IF EXISTS 'assignments_grades';  -- Drop 'assignments_grades' table if it already exists
CREATE TABLE 'assignments_grades' (         -- Create 'assignments_grades' with a unique ID, foreign keys for 'assignments' and 'students', grade, and date of grading
    grade_id INTEGER PRIMARY KEY,
    assisgnment_id INTEGER REFERENCES assignments(assisgnment_id),
    student_id INTEGER REFERENCES students(student_id),
    grade INTEGER,
    date varchar(255)
);
"""

# A list of random family names to use in generating full names for teachers and students
families = """Иванов
Васильев
Петров
Смирнов
Михайлов
Фёдоров
Соколов
Яковлев
Попов
Андреев
Алексеев
Александров
Лебедев
Григорьев
Степанов
Семёнов
Павлов
Богданов
Николаев
Дмитриев
Егоров
Волков
Кузнецов
Никитин
Соловьёв""".split()

# Letters to generate initials for the names
name_letters = "абвгдежзиклмнопрстуфхцчшщэюя".upper()

# Date format for random date generation
date_format = '%Y-%m-%d'

def _get_random_date(base_date: Optional[str] = None) -> str:
    """
    Generates a random date. If base_date is provided, the function modifies it by a few days. 
    Otherwise, it generates a random date in 2020.
    """
    if base_date is None:
        # Random day and month in 2020
        day = random.randint(1, 30)
        month = random.randint(1, 12)
        try:
            date = datetime.datetime(year=2020, month=month, day=day)
        except ValueError:
            # Handle potential invalid dates
            day -= 1
            date = datetime.datetime(year=2020, month=month, day=day)
    else:
        # Modifies the base date by a random number of days (-10 to +5)
        date = datetime.datetime.strptime(base_date, date_format)
        new_date = random.randint(-10, 5)
        if new_date < 0:
            date = date - datetime.timedelta(days=abs(new_date))
        else:
            date = date + datetime.timedelta(days=abs(new_date))
    return date.strftime(date_format)

def _get_random_full_name() -> str:
    """
    Generates a random full name using a family name and two initials.
    Adjusts the family name for gender if necessary.
    """
    is_male = random.choice((True, False))
    family_name = random.choice(families)
    if not is_male:
        # Add an 'а' at the end of the surname if the person is female
        family_name += "а"
    
    # Random initials from 'name_letters'
    first_letter, last_letter = random.choice(name_letters), random.choice(name_letters)
    return f"{family_name} {first_letter}.{last_letter}."

# Lists of verbs and nouns to create random assignment descriptions
assignment_verbs = """
посчитать
написать
сочинить
прочитать
выучить
изучить
описать
посетить
деконструировать
апробировать
проанализировать
прочувствовать
переписать
""".split()

assignment_nouns = """алгоритмы и структуры данных
история мировых цивилизаций
хлебобулочные изделия
виноградники в Англии
путешествия во времени
быстродействие исчислений на счетах
классику киноч
основы программирования
базы данных
язык запросов SQL
""".split('\n')

def _get_random_assignment_text() -> str:
    """
    Generates a random assignment description by combining a verb and a noun.
    """
    return f'{random.choice(assignment_verbs)} {random.choice(assignment_nouns)}'

def generate_database():
    """
    Creates the 'homework.sqlite' database, creates tables, and populates them with random data.
    """
    # Connect to SQLite database
    with sqlite3.connect('homework.sqlite') as conn:
        cursor = conn.cursor()
        
        # Execute the script to create tables
        cursor.executescript(CREATE_DATABASE_QUERY)
        conn.commit()

        # Generate random teacher data (10 teachers)
        teachers = [
            (_get_random_full_name(),) for _ in range(10)
        ]
        conn.executemany(
            """
            INSERT INTO 'teachers'(full_name)
            VALUES (?)
            """,
            teachers
        )

        # Generate random student groups, each associated with a teacher (20 groups)
        groups = [(random.randint(1, 20),) for _ in range(20)]
        conn.executemany(
            """
            INSERT INTO 'students_groups'(teacher_id)
            VALUES(?)
            """,
            groups
        )

        # Generate random students (400 students), each assigned to a group
        students = [
            (_get_random_full_name(), random.randint(1, 20)) for _ in range(400)
        ]
        conn.executemany(
            """
            INSERT INTO 'students'(full_name, group_id)
            VALUES(?, ?)
            """,
            students
        )

        # Generate random assignments (40 assignments) for random teachers and groups
        assignments = [
            (
                random.randint(1, 10),  # Random teacher ID
                _get_random_date(),     # Random due date
                random.randint(1, 20),  # Random group ID
                _get_random_assignment_text(),  # Random assignment text
            )
            for _ in range(40)
        ]
        conn.executemany(
            """
            INSERT INTO 'assignments'(teacher_id, due_date, group_id, assignment_text)
            VALUES(?, ?, ?, ?)
            """,
            assignments
        )

        # Generate random grades for each assignment (each assignment gets 20 random grades)
        assignments_grades = [
            (
                random.randint(1, 40),  # Random assignment ID
                random.randint(1, 400),  # Random student ID
                int(random.uniform(0.0, 10.99)),  # Random grade (0 to 10)
                _get_random_date(asgn[1])  # Random date near assignment due date
            )
            for asgn in assignments
            for _ in range(20)  # Each assignment gets 20 grades
        ]
        conn.executemany(
            """
            INSERT INTO 'assignments_grades'(assisgnment_id, student_id, grade, date)
            VALUES(?, ?, ?, ?)
            """,
            assignments_grades
        )

# If the script is run as the main program, generate the database
if __name__ == '__main__':
    generate_database()
