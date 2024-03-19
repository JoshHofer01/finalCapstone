# Task Manager

### **Contents**
    Description
    Installation
    Usage

### Description:
This command line application was created as a final project for my Software Engineering bootcamp with <a title="View Josh's Bootcamp Portfolio" href="https://www.hyperiondev.com/portfolio/JO23090009573/">Hyperion Dev</a>. The programm is a culmination of a majority of the skills taught to us since November 25th 2023, such as File I/O, error handling, and function modulation.

It implements a functional task management system in Python. File I/O operations for data persistence actively update csv files created by the app to ensure a streamline experience for the user. The programm uses error handling and message validation to add robustness to the programm. This app is designed with UX in mind.

### Installation:
1. Create a local folder named "Task Manager CLI".
2. Open terminal/command prompt and *cd* to your newly created folder.
3. Change directory to "Task Manager CLI" folder in git bash & initialize folder using *git init*.
4. Still using git bash, type "*git clone https://github.com/JoshHofer01/finalCapstone.git*"
5. Open folder in VSCode using "*code .*", or in your IDE of choice.
    + All libraries used are built-in python libraries, no *requirements.txt* or installation of external libraries is needed.

### Usage:
After cloning the repository, executing *'task_manager.py'* creates *'user.txt'* & *task.txt* files with the existing login information as **admin/password**. Using these credentials, users can login to the admin panel of the programm and create an additional account.
After logging in, users are presented with a menu, from where tasks can be added, updated, deleted, moved to a new user, and viewed, as well viewing the statistics of the programm such as how many tasks have been created and how many users are registered.

+ **Notes:**
    + Do not delete or change the admin username, this is the only user that will have admin access to the programm and can generate reports.