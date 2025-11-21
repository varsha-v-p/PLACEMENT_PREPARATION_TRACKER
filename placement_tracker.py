# placement_tracker_ui.py
import mysql.connector
from datetime import datetime

# ------------------- DATABASE CONNECTION -------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Varsha@13",
    database="placement_tracker"
)
cursor = conn.cursor()

# ------------------- HELPER: clear pending stored-proc results -------------------
def clear_results():
    try:
        res = cursor.stored_results
        if callable(res):
            for r in res():
                try:
                    r.fetchall()
                except:
                    pass
        else:
            for r in res:
                try:
                    r.fetchall()
                except:
                    pass
    except:
        pass

# ------------------- FUNCTIONS -------------------

def add_student():
    clear_results()
    print("\n--- Add New Student ---")
    st_id = int(input("Enter Student ID: "))
    name = input("Enter Name: ").strip()
    branch = input("Enter Branch: ").strip()
    year = int(input("Enter Year (1-4): "))
    mail = input("Enter Email: ").strip()
    cursor.execute("INSERT INTO Student VALUES (%s, %s, %s, %s, %s)",
                   (st_id, name, branch, year, mail))
    conn.commit()
    print("Student added successfully.")

def view_students():
    clear_results()
    print("\n--- All Students ---")
    cursor.execute("SELECT * FROM Student")
    rows = cursor.fetchall()
    if not rows:
        print("No students found.")
        return
    print(f"{'ID':<5} {'Name':<25} {'Branch':<10} {'Year':<5} {'Email'}")
    print("-" * 80)
    for r in rows:
        print(f"{r[0]:<5} {r[1]:<25} {r[2]:<10} {r[3]:<5} {r[4]}")
    print("-" * 80)

def add_goal():
    clear_results()
    print("\n--- Add Preparation Goal ---")
    goal_id = int(input("Enter Goal ID: "))
    st_id = int(input("Enter Student ID: "))
    title = input("Enter Goal Title: ").strip()
    desc = input("Enter Description: ").strip()
    status = input("Enter Status (Pending/In Progress/Completed): ").strip()
    cursor.execute("INSERT INTO Preparation_Goal VALUES (%s, %s, %s, %s, %s)",
                   (goal_id, st_id, title, desc, status))
    conn.commit()
    print("Goal added successfully.")

def view_goals():
    clear_results()
    print("\n--- View Goals for Student ---")
    st_id = int(input("Enter Student ID: "))
    cursor.execute("SELECT Goal_Id, Goal_Title, Description, Status FROM Preparation_Goal WHERE St_Id=%s", (st_id,))
    rows = cursor.fetchall()
    if not rows:
        print("No goals found for this student.")
        return
    print(f"{'Goal ID':<10} {'Title':<35} {'Status':<15}")
    print("-" * 70)
    for r in rows:
        title = (r[1][:32] + '...') if len(r[1]) > 35 else r[1]
        print(f"{r[0]:<10} {title:<35} {r[3]:<15}")
    print("-" * 70)

def update_goal():
    clear_results()
    print("\n--- Update Preparation Goal ---")
    goal_id = int(input("Enter Goal ID to update: "))
    print("1. Update Title")
    print("2. Update Description")
    print("3. Update Status")
    choice = input("Choose (1/2/3): ").strip()

    if choice == '1':
        new_title = input("Enter new title: ").strip()
        cursor.execute("UPDATE Preparation_Goal SET Goal_Title=%s WHERE Goal_Id=%s", (new_title, goal_id))
    elif choice == '2':
        new_desc = input("Enter new description: ").strip()
        cursor.execute("UPDATE Preparation_Goal SET Description=%s WHERE Goal_Id=%s", (new_desc, goal_id))
    elif choice == '3':
        new_status = input("Enter new status: ").strip()
        cursor.execute("UPDATE Preparation_Goal SET Status=%s WHERE Goal_Id=%s", (new_status, goal_id))
    else:
        print("Invalid option.")
        return

    conn.commit()
    print("Goal updated successfully.")

def add_mock():
    clear_results()
    print("\n--- Add Mock Interview ---")
    interview_id = int(input("Enter Interview ID: "))
    st_id = int(input("Enter Student ID: "))
    date = input("Enter Date (YYYY-MM-DD): ").strip()
    type_ = input("Enter Type: ").strip()
    cursor.execute("INSERT INTO Mock_Interview VALUES (%s, %s, %s, %s)",
                   (interview_id, st_id, date, type_))
    conn.commit()
    print("Mock Interview added successfully.")

def view_mock():
    clear_results()
    print("\n--- View Mock Interviews ---")
    st_id = int(input("Enter Student ID: "))

    cursor.callproc('Show_Mock_Interviews', [st_id])

    try:
        iterable = cursor.stored_results()
    except TypeError:
        iterable = cursor.stored_results

    rows_total = []
    for r in iterable:
        rows = r.fetchall()
        if rows:
            rows_total.extend(rows)

    if not rows_total:
        print("No mock interviews found.")
        return

    print(f"{'Interview ID':<15} {'Student Name':<25} {'Date':<12} {'Type':<12}")
    print("-" * 70)

    for row in rows_total:
        if len(row) == 3:
            name, date_val, typ = row
            date_str = date_val.strftime("%Y-%m-%d")
            print(f"{'':<15} {name:<25} {date_str:<12} {typ:<12}")
        else:
            interview_id = row[0]
            date_val = row[2]
            typ = row[3]
            cursor.execute("SELECT Name FROM Student WHERE St_Id=%s", (row[1],))
            name = cursor.fetchone()[0]
            date_str = date_val.strftime("%Y-%m-%d")
            print(f"{interview_id:<15} {name:<25} {date_str:<12} {typ:<12}")
    print("-" * 70)

def add_skill():
    clear_results()
    print("\n--- Add Skill ---")
    skill_id = int(input("Enter Skill ID: "))
    name = input("Enter Skill Name: ").strip()
    cursor.execute("INSERT INTO Skills VALUES (%s, %s)", (skill_id, name))
    conn.commit()
    print("Skill added successfully.")

def view_skills():
    clear_results()
    print("\n--- All Skills ---")
    cursor.execute("SELECT * FROM Skills")
    rows = cursor.fetchall()
    print(f"{'Skill ID':<10}{'Skill Name'}")
    print("-" * 40)
    for r in rows:
        print(f"{r[0]:<10}{r[1]}")
    print("-" * 40)

def update_skill_progress():
    clear_results()
    print("\n--- Update Skill Progress ---")
    st_id = int(input("Enter Student ID: "))
    skill_id = int(input("Enter Skill ID: "))
    level = input("Enter Level: ")
    last_updated = datetime.now().strftime("%Y-%m-%d")
    result = input("Enter Result (Pass/Fail): ")
    cursor.execute("""
        REPLACE INTO Student_Skill_Progress VALUES (%s, %s, %s, %s, %s)
    """, (st_id, skill_id, level, last_updated, result))
    conn.commit()
    print("Skill progress updated successfully.")

def view_skill_progress():
    clear_results()
    print("\n--- Skill Progress for Student ---")
    st_id = int(input("Enter Student ID: "))
    cursor.execute("""
        SELECT sk.Name, sp.Proficiency_Level, sp.Last_Updated, sp.Result
        FROM Student_Skill_Progress sp
        JOIN Skills sk ON sp.Skill_Id = sk.Skill_Id
        WHERE sp.St_Id=%s
    """, (st_id,))
    rows = cursor.fetchall()
    print(f"{'Skill Name':<30}{'Level':<15}{'Last Updated':<15}{'Result'}")
    print("-" * 80)
    for r in rows:
        print(f"{r[0]:<30}{r[1]:<15}{r[2]:<15}{r[3]}")
    print("-" * 80)

def add_test():
    clear_results()
    print("\n--- Add Test ---")
    test_id = int(input("Enter Test ID: "))
    difficulty = input("Enter Difficulty: ")
    subject = input("Enter Subject: ")
    date = input("Enter Date (YYYY-MM-DD): ")
    duration = int(input("Enter Duration (minutes): "))
    cursor.execute("INSERT INTO Test VALUES (%s, %s, %s, %s, %s)",
                   (test_id, difficulty, subject, date, duration))
    conn.commit()
    print("Test added successfully.")

def view_tests():
    clear_results()
    print("\n--- All Tests ---")
    cursor.execute("SELECT * FROM Test")
    rows = cursor.fetchall()
    print(f"{'Test ID':<10}{'Difficulty':<12}{'Subject':<25}{'Date':<12}{'Duration'}")
    print("-" * 80)
    for r in rows:
        print(f"{r[0]:<10}{r[1]:<12}{r[2]:<25}{r[3]:<12}{r[4]}")
    print("-" * 80)

def add_test_result():
    clear_results()
    print("\n--- Add Student Test Result ---")
    st_id = int(input("Enter Student ID: "))
    test_id = int(input("Enter Test ID: "))
    score = int(input("Enter Score: "))
    attempt_date = input("Enter Attempt Date (YYYY-MM-DD): ")
    result = "Pass" if score >= 50 else "Fail"
    cursor.execute("""
        REPLACE INTO Student_Test_Performance VALUES (%s, %s, %s, %s, %s)
    """, (st_id, test_id, score, attempt_date, result))
    conn.commit()
    print("Test result added successfully.")

def view_test_results():
    clear_results()
    print("\n--- View Test Results ---")
    st_id = int(input("Enter Student ID: "))
    cursor.execute("SELECT * FROM Student_Test_Performance WHERE St_Id=%s", (st_id,))
    rows = cursor.fetchall()
    print(f"{'Test ID':<10}{'Score':<10}{'Attempt Date':<15}{'Result'}")
    print("-" * 50)
    for r in rows:
        print(f"{r[1]:<10}{r[2]:<10}{r[3]:<15}{r[4]}")
    print("-" * 50)

def update_test_marks():
    clear_results()
    print("\n--- Update Test Marks ---")
    st_id = int(input("Enter Student ID: "))
    test_id = int(input("Enter Test ID: "))
    new_score = int(input("Enter New Score: "))
    new_result = "Pass" if new_score >= 50 else "Fail"
    cursor.execute("""
        UPDATE Student_Test_Performance
        SET Score=%s, Result=%s
        WHERE St_Id=%s AND Test_Id=%s
    """, (new_score, new_result, st_id, test_id))
    conn.commit()
    print("Test marks updated successfully.")

def avg_score():
    clear_results()
    print("\n--- Average Test Score ---")
    st_id = int(input("Enter Student ID: "))
    cursor.execute("SELECT Get_Avg_Score(%s)", (st_id,))
    avg = cursor.fetchone()[0]
    print(f"Average Score: {avg:.2f}")

# ------------------- NEW FEATURE 1 (NESTED QUERY) -------------------
def students_completed_all_goals():
    clear_results()
    print("\n--- Students Who Completed ALL Goals (Nested Query) ---")

    cursor.execute("""
        SELECT s.St_Id, s.Name
        FROM Student s
        WHERE s.St_Id IN (
            SELECT St_Id
            FROM Preparation_Goal
            GROUP BY St_Id
            HAVING SUM(Status = 'Completed') = COUNT(*)
        );
    """)

    rows = cursor.fetchall()
    if not rows:
        print("No student has completed all goals.")
        return

    print(f"{'Student ID':<12}{'Name'}")
    print("-" * 40)
    for r in rows:
        print(f"{r[0]:<12}{r[1]}")
    print("-" * 40)

# ------------------- NEW FEATURE 2 (AGGREGATE QUERY) -------------------
def test_statistics():
    clear_results()
    print("\n--- Test Statistics (Aggregate Query) ---")

    cursor.execute("""
        SELECT s.St_Id, s.Name,
               SUM(p.Result='Pass') AS Passed,
               SUM(p.Result='Fail') AS Failed
        FROM Student s
        LEFT JOIN Student_Test_Performance p ON s.St_Id = p.St_Id
        GROUP BY s.St_Id, s.Name;
    """)

    rows = cursor.fetchall()

    print(f"{'Student ID':<12}{'Name':<25}{'Passed':<10}{'Failed'}")
    print("-" * 60)

    for r in rows:
        passed = r[2] if r[2] is not None else 0
        failed = r[3] if r[3] is not None else 0
        print(f"{r[0]:<12}{r[1]:<25}{passed:<10}{failed}")

    print("-" * 60)


# ------------------- MAIN MENU -------------------
def main():
    while True:
        clear_results()
        print("\n==================== PLACEMENT PREPARATION TRACKER ====================")
        print("1.  Add Student")
        print("2.  View All Students")
        print("3.  Add Preparation Goal")
        print("4.  View Preparation Goals")
        print("5.  Update Preparation Goal")
        print("6.  Add Mock Interview")
        print("7.  View Mock Interviews")
        print("8.  Add Skill")
        print("9.  View All Skills")
        print("10. Update Skill Progress")
        print("11. View Skill Progress")
        print("12. Add Test")
        print("13. View All Tests")
        print("14. Add Test Result")
        print("15. View Test Results")
        print("16. Update Test Marks")
        print("17. Calculate Average Score")
        print("18. Students Completed All Goals")
        print("19. Test Statistics ")
        print("20. Exit")
        print("=========================================================================")

        ch = input("\nEnter your choice: ").strip()

        if ch == '1': add_student()
        elif ch == '2': view_students()
        elif ch == '3': add_goal()
        elif ch == '4': view_goals()
        elif ch == '5': update_goal()
        elif ch == '6': add_mock()
        elif ch == '7': view_mock()
        elif ch == '8': add_skill()
        elif ch == '9': view_skills()
        elif ch == '10': update_skill_progress()
        elif ch == '11': view_skill_progress()
        elif ch == '12': add_test()
        elif ch == '13': view_tests()
        elif ch == '14': add_test_result()
        elif ch == '15': view_test_results()
        elif ch == '16': update_test_marks()
        elif ch == '17': avg_score()
        elif ch == '18': students_completed_all_goals()
        elif ch == '19': test_statistics()
        elif ch == '20':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        main()
    finally:
        cursor.close()
        conn.close()
