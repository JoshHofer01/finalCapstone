# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date
import csv


DATETIME_STRING_FORMAT = "%Y-%m-%d"
# Create current date object, give correct time formatting
# return correct time format to datetime object for comparisons
current_date = datetime.now().date().strftime(DATETIME_STRING_FORMAT)
current_date = datetime.strptime(current_date, DATETIME_STRING_FORMAT)
# global data structures used within main and other functions
username_password = {}
task_list = []

def main():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]


    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    #====Login Section====
    '''This code reads usernames and password from the user.txt file to 
        allow a user to login.'''
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    logged_in = False
    while not logged_in:

        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    while True:
        # presenting the menu to the user and 
        # making sure that the user input is converted to lower case.
        print()
        if curr_user == "admin":
            menu = input('''Select one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - Generate reports
        ds - Display statistics
        e - Exit
        : ''').lower()
        else:
            menu = input('''Select one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        ds - Display statistics
        e - Exit
        : ''').lower()
        

        if menu == 'r':
            reg_user()
        elif menu == 'a':
            add_task()
        elif menu == 'va':
            view_all()
        elif menu == 'vm':
            view_mine(curr_user)
        elif menu == "gr":
            if curr_user != "admin":
                print("You do not have clearance for this option")
            else:
                generate_reports()
        elif menu == 'ds' and curr_user == 'admin': 
            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            num_users = len(username_password.keys())
            num_tasks = len(task_list)

            print("-----------------------------------")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print("-----------------------------------")    
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")
        

def pct(value):
    return f"{int(value)}%"

"""
registers a new user and saves to user.txt. Checks if username is already in use
"""
def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    while True:
        try:
            new_username = input("New Username: ")
            if len(new_username) >= 3 and len(new_username) <= 15:
                with open("user.txt", "r") as in_file:
                    next(in_file)
                    for row in in_file:
                        # check if username is already in use
                        if new_username == row.strip().split(";")[0]:
                            print("Username already in use")
                            new_username = False
                            break
            else:
                print("Username should be between 3-15 characters in length")
            if new_username:
                break        
        except:
            print("These characters cannot be used in usernames!")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
            return

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")
        return


"""
Allow a user to add a new task to task.txt file
Prompt a user for the following: 
- A username of the person whom the task is assigned to,
- A title of a task,
- A description of the task and 
- the due date of the task.
"""
def add_task():
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        else:
            break

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")
    return


def generate_reports():
    """Creates default 'tasks' and 'users' file if these have not already
    been made within the programm. Programm will ignore creation of default
    files if files already exist in target location."""
    if not os.path.exists("tasks.txt"):
        with open('tasks.txt', "w") as default_tasks:
            default_tasks.write("admin;Add functionality to task manager;Add additional options and refactor the code.;2022-12-01;2022-11-22;No")

    if not os.path.exists("user.txt"):
        with open('users.txt', "w") as default_users:
            default_users.write("admin;password")

    # TASK_LIST = Global task list
    # TASK_INFO = Local variable
    # Creates dictionary for task and user info that
    # will get filled each time generate reports is ran
    task_info = {}
    user_info = []

    # Collect user information overview data
    user_count = 0
    task_count = 0

    # Declares dict keys here so that in output csv this header will be first
    task_info["task_count"] = 0
    task_info["completed"] = 0
    task_info["incomplete"] = 0
    task_info["overdue"] = 0

    for task in task_list:
        task_count += 1
        if task['completed'] == True:
            task_info["completed"] += 1
        else:
            task_info["incomplete"] += 1
        if current_date > task['due_date']:
            task_info["overdue"] += 1

    for profile in username_password:
        # Temp dict to store task count assigned to each user
        temp_user_info = {}
        user_count += 1
        # Compile necessary info
        temp_user_info["name"] = profile
        temp_user_info["tasks_assigned"] = 0
        completed = 0
        overdue = 0
        # Checks global TASK LIST
        # Checks against username and updates each users task count accordingly
        for i in range(task_count):
            if task_list[i]["username"] == temp_user_info["name"]:
                temp_user_info["tasks_assigned"] += 1
                if task_list[i]["completed"] == True:
                    completed += 1
                if task_list[i]["due_date"] < current_date:
                    overdue += 1

        # Turn variables created into dict key/value pairs
        # Account for if user has 0 tasks
        # Turns everything into percent value
        try:
            temp_user_info["tasks_assigned_pct"] = (temp_user_info["tasks_assigned"] / task_count) * 100
        except ZeroDivisionError:
            temp_user_info["tasks_assigned_pct"] = 0

        try:
            temp_user_info["tasks_completed"] = (completed / temp_user_info["tasks_assigned"]) * 100
        except ZeroDivisionError:
            temp_user_info["tasks_completed"] = 0

        if temp_user_info["tasks_assigned"] == 0:
            temp_user_info["tasks_incomplete"] = 0
        else:
            temp_user_info["tasks_incomplete"] = 100 - temp_user_info["tasks_completed"]

        try:
            temp_user_info["overdue"] = (overdue / temp_user_info["tasks_assigned"]) * 100
        except ZeroDivisionError:
             temp_user_info["overdue"] = 0
        
        user_info.append(temp_user_info) # Add dict to list of dicts
    task_info["task_count"] = task_count

    # UPDATE ITEMS IN USER INFO DICTIONARY THAT ARE 
    # BEING OUTPUT AS PERCENTAGES. USES CUSTOM FUNCTION (pct)
    for ea_dict in user_info:
        for key in ['tasks_assigned_pct', 'tasks_completed', 'tasks_incomplete', 'overdue']:
            ea_dict[key] = pct(ea_dict[key])

    # Write task_overview txt file with necessary information
    # Uses keys in task_info dictionary as headers
    with open("task_overview.txt", "w") as task_overview_out:
        task_overview_out.write(f"Task Count: \t\t {task_info['task_count']}\n")
        task_overview_out.write(f"Completed Tasks: \t {task_info['completed']}\n")
        task_overview_out.write(f"Incomplete Tasks: \t {task_info['incomplete']}\n")
        task_overview_out.write(f"Overdue Tasks: \t\t {task_info['overdue']}\n")
        task_overview_out.write(f"Incomplete %: \t\t {pct((task_info['incomplete'] / len(task_list)) * 100)}\n")
        task_overview_out.write(f"Overdue %: \t\t\t {pct((task_info['overdue'] / len(task_list)) * 100)}\n")
    print("\nTASK OVERVIEW HAS BEEN WRITTEN TO DISC")

    # Compile gathered data into out file
    with open("user_overview.txt", "w", newline="") as user_overview_out:
        #Write total tasks in programma
        user_overview_out.write(f"User Count: {user_count}\n")
        user_overview_out.write(f"Total Task Count: {task_count}\n")
        user_overview_out.write("\n")

        for ea_user in user_info:
            user_overview_out.write(f"STATS OVERVIEW FOR: {ea_user['name']}\n")
            user_overview_out.write(f"Tasks Assigned: \t {ea_user['tasks_assigned']}\n")
            user_overview_out.write(f"% of Tasks: \t\t {ea_user['tasks_assigned_pct']}\n")
            user_overview_out.write(f"Tasks Complete: \t {ea_user['tasks_completed']}\n")
            user_overview_out.write(f"Tasks Incomplete: \t {ea_user['tasks_incomplete']}\n")
            user_overview_out.write(f"Overdue Tasks: \t\t {ea_user['overdue']}\n")
            user_overview_out.write(f"\n") # New space for next user
    print("USER OVERVIEW HAS BEEN WRITTEN TO DISC")
    


"""
Reads the task from task.txt file and prints to the console in the 
format of Output 2 presented in the task pdf (i.e. includes spacing
and labelling) 
"""
def view_all():
    task_count = len(task_list)
    if task_list:
        print(f"\nTask count: {task_count}")
        for number, t in enumerate(task_list):
            print(f"Task {number}: {t['title']} (Completed: {t['completed']})")
        print("-1: Return to main menu")

        # Ask user for number and validate input    
        while True:
            try:
                choice = int(input("Select a tasks number: "))
            except ValueError:
                print(f"Please enter a valid numeric value.")
            if choice >= 0 and choice < task_count:
                break
            elif choice == -1:
                return
        task = task_list[choice]

        print("--------------------------------------------------------")
        print(f"Task {number}: \t\t {task['title']}")
        print(f"Assigned to: \t\t {task['username']}")
        print(f"Date Assigned: \t\t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date: \t\t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Task Description: \n {task['description']}")
        if task['completed']:
            print(f"Task Completed: \t\t Yes")
        else:
            print(f"Task Completed: \t\t No")
        print("--------------------------------------------------------")

    else:
        print("No current tasks")
        return
    

"""
Reads the task from task.txt file and prints to the console in the 
format of Output 2 presented in the task pdf (i.e. includes spacing
and labelling)
"""
def view_mine(curr_user):
    current_users_tasks = []
    for task in task_list:
        if task['username'] == curr_user:
            current_users_tasks.append(task)
    task_count = len(current_users_tasks)

    for number, t in enumerate(current_users_tasks):
        print(f"Task {number}: {t['title']} (Completed: {t['completed']})")
    print("-1: Return to main menu")

     # Ask user for number and validate input    
    while True:
        try:
            choice = int(input("Select a tasks number: "))
        except ValueError:
            print(f"Please enter a valid numeric value.")
        if choice >= 0 and choice < task_count:
            break
        elif choice == -1:
            return
    task = current_users_tasks[choice]
        
    print("--------------------------------------------------------")
    print(f"Task {number}: \t\t {task['title']}")
    print(f"Assigned to: \t\t {task['username']}")
    print(f"Date Assigned: \t\t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Due Date: \t\t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Task Description: \n {task['description']}")
    if task['completed']:
        print(f"Task Completed: \t\t Yes")
        return
    else:
        print(f"Task Completed: \t\t No")
    print("--------------------------------------------------------")
        
    # Ask user if task has been completed and updates task dictionary 
    while True:
        try:
            isCompleted = input("Is this task completed? (Yes/No): ").lower().strip()
            if isCompleted == 'yes' or isCompleted == 'no':
                break
            print("Please type (Yes/No)")
        except:
            print("Please type (Yes/No)")


    if isCompleted == "yes":
        global_index_choice = task_list.index(current_users_tasks[choice])
        # Update local and global task lists
        current_users_tasks[choice]['completed'] = True
        task_list[global_index_choice]['completed'] = True

        # Write new tasks file (Effectively updates with new info)
        with open("tasks.txt", "w") as tasks_file:
            for task in task_list:
                items = [item for item in task.values()]
                if task['completed']:
                    completion = "Yes"
                else:
                    completion = "No"
                # Write new line in correct format with new line symbol
                fmt_due = items[3].strftime(DATETIME_STRING_FORMAT)
                fmt_assigned = items[4].strftime(DATETIME_STRING_FORMAT)
                new_line = f"{';'.join(items[:3])};{fmt_due};{fmt_assigned};{completion}\n"
                tasks_file.write(new_line)

        print("\nUPDATED tasks.txt")
        return
        
    # User can edit their tasks to change the user task is assigned to and due date
    # Only shows up if task is NOT completed
    while True:
        try:
            edit_task = input("Would you like to edit this task? (Yes/No): ").lower().strip()
            if edit_task == 'yes' or edit_task == 'no':
                if edit_task == 'no':
                    edit_task = False
                    break
                break
            print("Please type (Yes/No)")
        except:
            print("Please type (Yes/No)")

    if edit_task:
        assigned_date = current_users_tasks[choice]['assigned_date'].strftime(DATETIME_STRING_FORMAT)
        due_date = current_users_tasks[choice]['due_date'].strftime(DATETIME_STRING_FORMAT)
        old_row = f"{current_users_tasks[choice]['username']};{current_users_tasks[choice]['title']};{current_users_tasks[choice]['description']};{due_date};{assigned_date};No\n"
        while True:
            task_username = input("Name of person assigned to task: ")
            if task_username not in username_password.keys():
                print("User does not exist. Please enter a valid username")
                continue
            else:
                current_users_tasks[choice]['name'] = task_username
                break
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                if current_date > due_date_time:
                    print("Due date cannot be in the past")
                else:
                    current_users_tasks[choice]['due_date'] = due_date_time
                    break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Update tasks.txt with new information
        new_row = f"{task_username};{current_users_tasks[choice]['title']};{current_users_tasks[choice]['description']};{due_date_time.strftime(DATETIME_STRING_FORMAT)};{assigned_date};No\n"

        # Open file for use in updating tasks.txt if edits are made
        with open("tasks.txt", "r") as tasks_file:
            lines = tasks_file.readlines()
        
        # Update file with correct new information
        for i in range(len(lines)):
            print(lines[i])
            if lines[i] == old_row:
                lines[i] = new_row

        # Write new tasks file (Effectively updates with new info)
        with open("tasks.txt", "w") as tasks_file:
            tasks_file.writelines(lines)

        print("\nUPDATED tasks.txt")
        return
        

if __name__ == "__main__":
    main()