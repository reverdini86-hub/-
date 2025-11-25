import sqlite3
import datetime
import sys

def sozdanie_baz():
    BD = sqlite3.connect("spravochnik_po_boleznyam.BD")
    cursor = BD.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Diseases (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, recomendations TEXT, symptoms TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Patients (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, phone TEXT, passpoet TEXT")
    cursor.execute("CREATE TABLE IF NOT EXISTS Doctors (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, speciality TEXT, phone TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS History (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, disease_id INTEGER, appointments_id INTEGER date_start TEXT, date_end TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER recomendations TEXT, symptoms TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT, password TEXT, role TEXT, link_id INTEGER)")
    BD.commit()
    return BD

def registrasiya_user(BD):
    print("Создатель: Анастасия" \
    "\n --- Регистрация пользователя ---")

    login = input(f"Введите логин: ")
    password = input("Введите пароль: ")

    print("Выберите роль:")
    print("1 - Пациент")
    print("2 - Врач")
    print("3 - Администратор")

    kakaya_role = input("Введите номер: ")

    if kakaya_role == "1":

        role = "patient"
        full_name = input("ФИО: ")
        phone = input("Телефон: ")
        passport = input("Паспорт: ")
        cursor = BD.cursor()
        cursor.execute("(INSERT INTO Patients (full_name, phone, passport), VALUES (?, ?, ?)", (full_name, phone, passport))
        BD.commit()

        patient_id = cursor.lastrowid

        cursor.execute("INSERT INTO Users (login, password, role, link_id) VALUES (?, ?, ?, ?)", (login, password, role, patient_id))
        BD.commit()

        print("Пользователь зарегестирован. Добро пожаловать в справочник по болезням, дорогой пациент.")
    
    elif kakaya_role == "2":
        role = "doctor"
        full_name = input("ФИО: ")
        speciality = input("Специальность: ")
        phone = input("Телефон: ")

        cursor = BD.cursor()
        cursor.execute("INSERT INTO Doctors (full_name, speciality, phone) VALUES (?, ?, ?)", (full_name, speciality, phone))
        BD.commit()

        doctor_id = cursor.lastrowid

        cursor.execute("INSERT INTO Users(login, password, role, link_id) VALUES (?, ?, ?, ?)", (login, password, role, doctor_id))
        BD.commit()
        print("Пользователь зарегистрирован. Добро пожаловать в справочник по болезням, уважаемый Врач!")

    elif kakaya_role == "3":
        role = "admin"

        cursor = BD.cursor()
        cursor.execute("INSERT INTO Users (login, password, role, link_id) VALUES (?, ?, ?, ?)", login, password, "admin", 0 )
        BD.commit()

        print("Добро поаловать, Администратор!")

    else:
        print("Неверно были введены даннае. Пожалуйста, заполните их верно")

    def login_user(BD):
        print("Создатель: Анастасия")
        print("\n--- Вход в личный кабинет ---")

        login = input("Логин: ")
        password = input("Пароль: ")
        
        cursor = BD.cursor()
        cursor.execute("SELECT id, role, linl_id FROM Users WHERE login = ? AND password = ?", (login, password))
        user = cursor.fetchone()

        if user is None:
            print("Неверный логин или пароль. Введите пожалуйста правильно")
            return None
        user_id = user[0]
        role = user[1]
        link_id = user[2]
        return (user_id, role, link_id)
    
def menu_admina(BD):
    while True:
        print("n\--- Кабинет администратора ---")
        print("1 - Добавить заболевание")
        print("2 - Показать список заболеваний")
        print("3 - Добавить пациента")
        print("4 - Добавить врача")
        print("5 - Удалить запись на приём")
        print("6 - Показать все записи")
        print("0 - Выход из кабинета")

        kakoyi_choice = input("Введите номер: ")
        if kakoyi_choice == "1":
            add_disease(BD)
        elif kakoyi_choice == "2":
            show_diseases(BD)
        elif kakoyi_choice == "3":
            add_patient(BD)
        elif kakoyi_choice == "4":
            add_doctor(BD)
        elif kakoyi_choice == "5":
            show_all_appointment(BD)
        elif kakoyi_choice == "6":
            delete_appointment(BD)
        elif kakoyi_choice == "0":
            break
        else:
            print("Неверный ввод. Введите пожалуйста число, которое есть в базе данных")

def add_disease(BD):
    print("n\--- Добавление заболевания ---")
    name = input("Название болезни")
    definition = input("Определение болезни: ")
    symptoms = input("Симптомы заболевшего: ")
    recomendatios = input(f"Рекомендации к выздоровлению пациента - лекарста, терапия, может что-то ещё")

    cursor = BD.cursor()
    cursor.execute("INSERT INTO Deseases (name, definition, recomendation, symptoms) VALUES (?, ?, ?, ?)", (name, definition, recomendatios, symptoms))
    BD.commit()

    print(f"Заболевание было успешно добавлено. Внимательно проверьте, не допустили ли в ошибку в добавлении нового параметра. Если допустили, то немедленно исправьте")

def show_diseases(BD):
    print("n\--- Список заболеваний ---")
    cursor = BD.cursor()
    cursor.execute("SELECT id, name FROM Diseases")
    rows = cursor.fetchall()

    for row in rows:
        print("ID:", row[0], " ", row[1])

def add_patient(BD):
    print("n\--- Добавить пациента ---")
    name = input("ФИО: ")
    phone = input("Телефон: ")
    passport = input("Паспорт: ")
    cursor = BD.cursor()
    cursor.execute("INSERT INTO Patients (full_name, phone, passport) VALUES (?, ?, ?)", (name, phone, passport))
    BD.commit()
    print("Пациент добавлен")

def patient_menu(BD, patient_id):
    while True:
        print("\n--- Кабинет пациента ---")
        print("1 - Просмотр заболеваний")
        print("2 - Записаться на приём")
        print("3 - Моя история болезней")
        print("0 - Выход из справочника по болезням")

        kakoyi_choice_patient = input("Введи номер: ")

        if kakoyi_choice_patient == "1":
            show_diseases(BD)
        elif kakoyi_choice_patient =="2":
            make_appointment(BD, patient_id)
        elif kakoyi_choice_patient =="3":
            show_patient_history(BD, patient_id)
        elif kakoyi_choice_patient =="0":
            break
        else:
            print("Были неверно введены данные")

def add_doctor(BD):
    print("\n--- Добавить врача ---")
    name = input("ФИО: ")
    speciality = input("Специальность: ")
    phone = input("Телефон: ")
    cursor = BD.cursor()
    cursor.execute("INSERT INTO Doctors (full_name, speciality, phone) VALUES (?, ?, ?)", (name, speciality, phone))
    BD.commit()
    print("Врач добавлен")

def doctor_menu(BD, doctor_id):
    while True:
        print("\n--- Кабинет врача ---")
        print("1 - Посмотреть текущие запись пациентов")
        print("2 - Добавить запись в историю болезней")
        print("0 - Выход")
        kakoyi_choice_vrach = input("Введите номер: ")
        if kakoyi_choice_vrach == "1":
            show_doctor_appointments(BD, doctor_id)
        elif kakoyi_choice_vrach == "2":
            add_history_record(BD, doctor_id)
        elif kakoyi_choice_vrach == "0":
            break
        else:
            print("Были неверно введены данные. Пожалуйста, введите ещё раз их")

def make_appointment(BD, patient_id):
    print("\n--- Запись на приём к врачу ---")
    cursor = BD.cursor()
    cursor.execute("SELECT id, full_name, speciality FROM Doctors")
    rows = cursor.fetchall()
    print("Список врачей: ")
    for d in rows:
        print(d[0], "-", d[1], "(", d[2], ")")
    doctor_id = input("Введите ID врача: ")
    date = input("Введите дату (ГГГГ-ММ-ДД): ")
    cursor.execute("INSERT INTO Appointments (patient_id, doctor_id, date, status) VALUES (?, ?, ?, ?)", (patient_id, doctor_id, date, "active"))
    BD.commit()
    print("Вы записаны")

