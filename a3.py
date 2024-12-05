from sqlalchemy import create_engine, text
from config import settings

engine = create_engine(
    settings.DATABASE_URL(),
)

print("o List all diseases caused by 'bacteria' that were discovered before 2020.")
with engine.connect() as con:
    query = """
       SELECT d.disease_code, d.description
       FROM Disease d
       JOIN Discover ds ON d.disease_code = ds.disease_code
       WHERE d.pathogen = 'Bacteria' AND ds.first_enc_date < '2020-01-01';
       """
    res = con.execute(text(query))
    for row in res:
        print(row)
    print()

    print("o Retrieve the names and degrees of doctors who are not specialized in “infectious diseases.”")
    query = """
        SELECT u.name, d.degree
        FROM Users u
        JOIN Doctor d ON d.email = u.email 
        WHERE u.email NOT IN(
            SELECT s.email
            FROM Specialize s
            JOIN DiseaseType dt ON s.id = dt.id
            WHERE dt.description = 'Infectious Disease'
        );
        """
    result = con.execute(text(query))
    for row in result:
        print(row)
    print()

    print("o List the name, surname and degree of doctors who are specialized in more than 2 disease types.")
    query = """
            SELECT u.name, u.surname, d.degree
            FROM Users u
            JOIN Doctor d ON d.email = u.email
            JOIN Specialize s ON d.email = s.email
            GROUP BY u.name, u.surname, d.degree
            HAVING COUNT(s.id) > 2;
           """
    res = con.execute(text(query))
    for row in res:
        print(row)
    print()

    print("o List countries and the average salary of doctors specialized in 'virology.'")
    query = """
            SELECT c.cname, AVG(u.salary) AS avg_salary
            FROM Users u
            JOIN Doctor d ON d.email = u.email
            JOIN Specialize s ON d.email = s.email
            JOIN Country c ON c.cname = u.cname
            JOIN DiseaseType dt on dt.id = s.id
            WHERE dt.description = 'virology'
            GROUP BY c.cname
           """
    res = con.execute(text(query))
    for row in res:
        print(row)
    print()

    print("o Find departments with public servants reporting \"covid-19\" cases across multiple countries, counting such "
          "employees per department.")
    query = """
            SELECT ps.department, COUNT(DISTINCT ps.email) AS employee_count
            FROM PublicServant ps
            JOIN Record r ON r.email = ps.email
            WHERE r.disease_code = 'COV19'
            GROUP BY ps.department
            HAVING COUNT(DISTINCT r.cname) > 1;
           """
    res = con.execute(text(query))
    for row in res:
        print(row)
    print()

    print("o Double the salary of public servants who have recorded more than three “covid-19” patients.")
    query = """
            UPDATE Users
            SET salary = salary * 2
            WHERE email IN(
                SELECT r.email 
                FROM Record r
                WHERE r.disease_code = 'COV19'
                GROUP BY r.email
                HAVING SUM(r.total_patients) > 3
            );
           """
    con.execute(text(query))
    print("Salaries updated successfully!")
    print()

    print("o Delete users whose name contains the substring “bek” or “gul.”")
    query = """
            DELETE FROM Users
            WHERE name LIKE '%bek%' OR name LIKE '%gul%'
           """
    con.execute(text(query))
    print("Users deleted successfully!")
    print()

    print("o Create a primary indexing on the “email” field in the Users table.")
    query = """
            CREATE UNIQUE INDEX idx_users_email ON Users(email);
            CREATE INDEX idx_disease_code ON Disease(disease_code);
           """
    con.execute(text(query))
    print("Indexing successful")
    print()

    print("o List the top 2 countries with the highest number of total patients recorded.")
    query = """
        SELECT r.cname, SUM(r.total_patients) AS total_patients
        FROM Record r
        GROUP BY r.cname
        ORDER BY total_patients DESC
        LIMIT 2;
         """
    result = con.execute(text(query))
    for row in result:
        print(row)
    print()

    print("Calculating total number of patients with COVID-19...")
    query = """
           SELECT COUNT(DISTINCT pd.email) AS total_covid_patients
           FROM PatientDisease pd
           JOIN Disease d ON pd.disease_code = d.disease_code
           WHERE d.description = 'COVID-19';
       """
    result = con.execute(text(query))
    total_covid_patients = result.fetchone()[0]
    print(f"Total number of COVID-19 patients: {total_covid_patients}")
    print()
    print("Creating view for patients and their diseases...")
    query = """
           CREATE OR REPLACE VIEW patient_disease_view AS
           SELECT u.name, u.surname, d.description AS disease
           FROM Users u
           JOIN Patients p ON u.email = p.email
           JOIN PatientDisease pd ON p.email = pd.email
           JOIN Disease d ON pd.disease_code = d.disease_code;
       """
    con.execute(text(query))
    print("View created successfully.")
    print()
    print("Retrieving data from the view")
    query = "SELECT * FROM patient_disease_view;"
    result = con.execute(text(query))
    for row in result:
        print(row)