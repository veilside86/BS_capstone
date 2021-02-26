import requests
import secrets
import sqlite3
from typing import Tuple
import pandas as pd


# def setup_db_excel(cursor: sqlite3.Cursor):
#     cursor.execute('''CREATE TABLE IF NOT EXISTS states(
#     occupation_title TEXT PRIMARY KEY,
#     state TEXT NOT NULL,
#     hourly_pct25_salary FLOAT,
#     annual_pct25_salary INTEGER,
#     occupation_code TEXT);
#     ''')


def save_excel_db(filename: str, conn):
    # for state_data in data:
    #     cursor.execute(
    #         """INSERT INTO states_data(state, occupation_title, hourly_pct25_salary, annual_pct25_salary,
    #         occupation_code) VALUES(?, ?, ?, ?, ?)""", state_data['area_title'], state_data['occ_title'],
    #         state_data['h_pct25'], state_data['a_pct25'], state_data['occ_code'])
    df = pd.read_excel(filename)
    df_subset = df[['area_title', 'occ_title', 'tot_emp', 'h_pct25', 'a_pct25', 'occ_code']]
    df_subset.to_sql(name='states', con=conn, if_exists='append', index=False)


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)   # connect to existing DB or create new one
    cursor = db_connection.cursor()     # get ready to read/write data
    return db_connection, cursor


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS schools(
    school_id INTEGER PRIMARY KEY,
    school_name TEXT NOT NULL,
    school_state TEXT NOT NULL,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER,
    student_size_2017 INTEGER,
    three_year_earnings_over_poverty INTEGER,
    repayment_overall INTEGER
    );''')
    # print('table created')


def close_db(connection: sqlite3.Connection):
    connection.commit()     # make sure any changes get saved
    connection.close()


def save_db(cursor, data):
    for school_data in data:
        cursor.execute(
            """INSERT INTO schools(school_id, school_name, school_state,
            school_city, student_size_2018, student_size_2017,
            three_year_earnings_over_poverty, repayment_overall) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
            (school_data['id'], school_data['school.name'], school_data['school.state'], school_data['school.city'],
             school_data['2018.student.size'], school_data['2017.student.size'],
             school_data['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
             school_data['2016.repayment.3_yr_repayment.overall']))


# def check_table(cursor: sqlite3.Cursor):
#     for row in cursor.fetchall():
#         print(row)


def get_data():
    final_data = []
    entire_data = True
    page = 0
    while entire_data:
        final_url = f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=" \
                    f"2,3&_fields=id,school.name,school.state,school.city,2018.student.size,2017.student.size,2017." \
                    f"earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment." \
                    f"overall&api_key={secrets.api_key}&page={page}"
        response = requests.get(final_url)
        if response.status_code != 200:
            print(response.text)
            return []
        json_data = response.json()
        page_data = json_data["results"]
        # initial_schools(cursor, page_data)
        final_data.extend(page_data)
        if len(page_data) < 20:
            entire_data = False
        page += 1

    return final_data


def save_data(data, filename='SchoolData.txt'):
    with open(filename, 'w') as file:
        for item in data:
            print(item, file=file)
        file.close()


def main():
    # max row 36383
    # url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=" \
    #       "2,3&_fields=id,school.name,school.state,school.city,2018.student.size,2017.student.size,2017." \
    #       "earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall"
    excel_file = "state_M2019_dl.xlsx"
    conn, cursor = open_db("school_db.sqlite")
    # conn, cursor = open_db("state_db.sqlite")
    # open_excel(filename)
    # dataframe = pd.read_excel(excel_file)
    # dataframe_subset = dataframe[['area_title', 'occ_title', 'h_pct25', 'a_pct25', 'occ_code']]
    # dataframe_subset.to_sql(name='states', con=conn, if_exists='append')
    # all_data = get_data()
    # save_data(all_data)
    # setup_db(cursor)
    # save_db(cursor, all_data)
    save_excel_db(excel_file, conn)
    close_db(conn)
    # print(states_subset)
    # print(all_data)


if __name__ == '__main__':
    main()
