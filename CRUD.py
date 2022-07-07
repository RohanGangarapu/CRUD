# CRUD program in Python
# CRUD users, projects and groups in database

#import statements
import sqlite3
import sys


# Connection of Database
conn = sqlite3.connect('role_manager.db')
c = conn.cursor()


# SQL Queries for creating tables in database
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, username TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS projects(projectID INTEGER PRIMARY KEY, projectname TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS groups(groupID INTEGER PRIMARY KEY, groupname TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS user_project(userID INTEGER, projectID INTEGER, role TEXT, PRIMARY KEY(userID, projectID))')
    c.execute('CREATE TABLE IF NOT EXISTS user_group(userID INTEGER, groupID INTEGER, PRIMARY KEY(userID, groupID))')
    c.execute('CREATE TABLE IF NOT EXISTS group_project(groupID INTEGER, projectID INTEGER, role TEXT, PRIMARY KEY(groupID, projectID))')
    print("Table Created!")
    conn.commit()


# For adding users in database
def add_user(username):
    c.execute('INSERT INTO users(username) VALUES(?)', (username,))
    print("User Added!")
    conn.commit()

# For adding projects in database
def add_project(projectname):
    c.execute('INSERT INTO projects(projectname) VALUES(?)', (projectname,))
    print("Project Added!")
    conn.commit()

# For adding groups in database
def add_group(groupname):
    c.execute('INSERT INTO groups(groupname) VALUES(?)', (groupname,))
    print("Group Added!")
    conn.commit()


# For options in role field
def get_role(roleID):
  if roleID == 1:
    return "Owner"
  elif roleID == 2:
    return "Admin"
  elif roleID == 3:
    return "Manager"
  elif roleID == 4:
    return "Employee"
  else:
    print("Wrong input in role field!")

def get_roleID(role):
  if role == "Owner":
    return 1
  elif role == "Admin":
    return 2
  elif role == "Manager":
    return 3
  elif role == "Employee":
    return 4
  else:
    print("Wrong input in roleID field!")


# For assigning user to project
def assign_user_project(username, projectname, roleID):
    c.execute('SELECT userID FROM users WHERE username = ?', (username,))
    userID = c.fetchone()[0]
    c.execute('SELECT projectID FROM projects WHERE projectname = ?', (projectname,))
    projectID = c.fetchone()[0]
    role = get_role(roleID)
    c.execute('INSERT INTO user_project(userID, projectID, role) VALUES(?, ?, ?)', (userID, projectID, role))
    print("Assigned!")
    conn.commit()

# For assigning user to group
def assign_user_group(username, groupname):
    c.execute('SELECT userID FROM users WHERE username = ?', (username,))
    userID = c.fetchone()[0]
    c.execute('SELECT groupID FROM groups WHERE groupname = ?', (groupname,))
    groupID = c.fetchone()[0]
    c.execute('INSERT INTO user_group(userID, groupID) VALUES(?, ?)', (userID, groupID))

    c.execute('SELECT projectID, role FROM group_project WHERE groupID = ?', (groupID,)) # For adding users in existing projects
    for row in c.fetchall():
      c.execute('SELECT projectname FROM projects where projectID = ?', (row[0],))
      projectname = c.fetchone()[0]
      roleID = int(get_roleID(row[1]))
      assign_user_project(username, projectname, roleID)
    print("Assigned!")
    conn.commit()

# For assigning group to project
def assign_group_project(groupname, projectname, roleID):
    c.execute('SELECT groupID FROM groups WHERE groupname = ?', (groupname,))
    groupID = c.fetchone()[0]
    c.execute('SELECT projectID FROM projects WHERE projectname = ?', (projectname,))
    projectID = c.fetchone()[0]
    role = get_role(roleID)
    c.execute('INSERT INTO group_project(groupID, projectID, role) VALUES(?, ?, ?)', (groupID, projectID, role))
    
    c.execute('SELECT userID FROM user_group WHERE groupID = ?', (groupID,)) # For adding existing users in project
    for row in c.fetchall():
      c.execute('SELECT username FROM users WHERE userID = ?', (row[0],))
      username = c.fetchone()[0]
      assign_user_project(username, projectname, roleID)
    print("Assigned!")
    conn.commit()


# For displaying projects and groups of user
def show_user(username):
    print("Projects (UserID, UserName, Project, Role) : ")
    c.execute('SELECT userID FROM users WHERE username = ?', (username,))
    userID = c.fetchone()[0]
    c.execute('SELECT projectID, role FROM user_project WHERE userID = ?', (userID,))
    for row in c.fetchall():
      c.execute('SELECT projectname FROM projects WHERE projectID = ?', (row[0],))
      projectname = c.fetchone()[0]
      role = row[1]
      print(userID, username, projectname, role)
    
    print("Groups (UserID, UserName, Group) : ")
    c.execute('SELECT groupID FROM user_group WHERE userID = ?', (userID,))
    for row in c.fetchall():
      c.execute('SELECT groupname FROM groups WHERE groupID = ?', (row[0],))
      groupname = c.fetchone()[0]
      print(userID, username, groupname)


# For displaying users and groups of project
def show_project(projectname):
    print("Users in project : ")
    c.execute('SELECT projectID FROM projects WHERE projectname = ?', (projectname,))
    projectID = c.fetchone()[0]
    c.execute('SELECT userID, role FROM user_project WHERE projectID = ?', (projectID,))
    for row in c.fetchall():
      c.execute('SELECT username FROM users WHERE userID = ?', (row[0],))
      username = c.fetchone()[0]
      # c.execute('SELECT role FROM user_project WHERE userID = ?', (row[0],))
      role = row[1]
      print(projectname, username, role)

    print("Groups belong to this project : -")
    c.execute('SELECT groupID FROM group_project WHERE projectID = ?', (projectID,))
    for row in c.fetchall():
      c.execute('SELECT groupname FROM groups WHERE groupID = ?', (row[0],))
      groupname = c.fetchone()[0]
      print(projectname, groupname)


# For displaying users and projects of group
def show_group(groupname):
    print("Users in group : ")
    c.execute('SELECT groupID FROM groups WHERE groupname = ?', (groupname,))
    groupID = c.fetchone()[0]
    c.execute('SELECT userID FROM user_group WHERE groupID = ?', (groupID,))
    for row in c.fetchall():
      c.execute('SELECT username FROM users WHERE userID = ?', (row[0],))
      username = c.fetchone()[0]
      print(username)
    
    print("Projects of group : ")
    c.execute('SELECT projectID FROM group_project WHERE groupID = ?', (groupID,))
    for row in c.fetchall():
      c.execute('SELECT projectname FROM projects WHERE projectID = ?', (row[0],))
      projectname = c.fetchone()[0]
      print(projectname)


# For printing all users
def show_all_users():
    c.execute('SELECT username, userID FROM users')
    for row in c.fetchall():
        print(row[1], row[0])

# For printing all projects
def show_all_projects():
    c.execute('SELECT projectname FROM projects')
    for row in c.fetchall():
        print(row[0])

# For printing all groups
def show_all_groups():
    c.execute('SELECT groupname FROM groups')
    for row in c.fetchall():
        print(row[0])


# For deleting the user and removing its projects and groups
def delete_user(username):
    c.execute('SELECT userID FROM users WHERE username = ?', (username,))
    userID = c.fetchone()[0]
    c.execute('DELETE FROM users WHERE userID = ?', (userID,))
    c.execute('DELETE FROM user_project WHERE userID = ?', (userID,))
    c.execute('DELETE FROM user_group WHERE userID = ?', (userID,))
    print("Deleted!")
    conn.commit()

# For deleting the project and removing the links with user and groups
def delete_project(projectname):
    c.execute('SELECT projectID FROM projects WHERE projectname = ?', (projectname,))
    projectID = c.fetchone()[0]
    c.execute('DELETE FROM projects WHERE projectID = ?', (projectID,))
    c.execute('DELETE FROM user_project WHERE projectID = ?', (projectID,))
    c.execute('DELETE FROM group_project WHERE projectID = ?', (projectID,))
    print("Deleted!")
    conn.commit()

# For deleting the group and removing its link with user and projects
def delete_group(groupname):
    c.execute('SELECT groupID FROM groups WHERE groupname = ?', (groupname,))
    groupID = c.fetchone()[0]
    c.execute('DELETE FROM groups WHERE groupID = ?', (groupID,))
    c.execute('DELETE FROM user_group WHERE groupID = ?', (groupID,))
    c.execute('DELETE FROM group_project WHERE groupID = ?', (groupID,))
    print("Deleted!")
    conn.commit()


# For removing specific user from project
def unassign_user_project(username, projectname):
    c.execute('SELECT userID FROM users WHERE username = ?', (username,))
    userID = c.fetchone()[0]
    c.execute('SELECT projectID FROM projects WHERE projectname = ?', (projectname,))
    projectID = c.fetchone()[0]
    c.execute('DELETE FROM user_project WHERE userID = ? AND projectID = ?', (userID, projectID))
    print("UnAssigned!")
    conn.commit()

# For removing specific user from group and group-related projects
def unassign_user_group(username, groupname):
    c.execute('SELECT userID FROM users WHERE username = ?', (username,))
    userID = c.fetchone()[0]
    c.execute('SELECT groupID FROM groups WHERE groupname = ?', (groupname,))
    groupID = c.fetchone()[0]
    c.execute('DELETE FROM user_group WHERE userID = ? AND groupID = ?', (userID, groupID))

    c.execute('SELECT projectID FROM group_project WHERE groupID = ?', (groupID,))
    for row in c.fetchall():
      c.execute('SELECT projectname FROM projects WHERE projectID = ?', (row[0],))
      projectname = c.fetchone()[0]
      unassign_user_project(username, projectname) # check again
    print("UnAssigned!")
    conn.commit()

# For removing specific group from project and users from that group
def unassign_group_project(groupname, projectname):
    c.execute('SELECT groupID FROM groups WHERE groupname = ?', (groupname,))
    groupID = c.fetchone()[0]
    c.execute('SELECT projectID FROM projects WHERE projectname = ?', (projectname,))
    projectID = c.fetchone()[0]
    c.execute('DELETE FROM group_project WHERE groupID = ? AND projectID = ?', (groupID, projectID))

    c.execute('SELECT userID FROM user_group WHERE groupID = ?', (groupID,))
    for row in c.fetchall():
      c.execute('SELECT username FROM users WHERE userID = ?', (row[0],))
      username = c.fetchone()[0]
      unassign_user_project(username, projectname) # check again
    print("UnAssigned!")
    conn.commit()


# For changing the role of user in projects
def change_role(username, projectname, roleID):
    c.execute('SELECT userID FROM users WHERE username = ?', (username,))
    userID = c.fetchone()[0]
    c.execute('SELECT projectID FROM projects WHERE projectname = ?', (projectname,))
    projectID = c.fetchone()[0]
    role = get_role(roleID)
    c.execute('UPDATE user_project SET role = ? WHERE userID = ? AND projectID = ?', (role, userID, projectID,))
    print("Changes Done!")
    conn.commit()

# For changing the role of group members in projects
def change_role_group(groupname, projectname, roleID):
    c.execute('SELECT groupID FROM groups WHERE groupname = ?', (groupname,))
    groupID = c.fetchone()[0]
    c.execute('SELECT projectID FROM projects WHERE projectname = ?', (projectname,))
    projectID = c.fetchone()[0]
    role = get_role(roleID)
    c.execute('UPDATE group_project SET role = ? WHERE groupID = ? AND projectID = ?', (role, groupID, projectID,))

    c.execute('SELECT userID FROM user_group WHERE groupID = ?', (groupID,))
    for row in c.fetchall():
      c.execute('SELECT username FROM users WHERE userID = ?', (row[0],))
      username = c.fetchone()[0]
      change_role(username, projectname, roleID)
    print("Changes Done!")
    conn.commit()


# MAIN METHOD
def main():
    create_table()
    while True:
        command = input('Enter command: ')
        if command.lower() == 'exit':
            sys.exit()
        
        elif command.lower() == 'add user':
            username = input('Enter user name: ')
            add_user(username)
        
        elif command.lower() == 'add project':
            projectname = input('Enter project name: ')
            add_project(projectname)
        
        elif command.lower() == 'add group':
            groupname = input('Enter group name: ')
            add_group(groupname)
        
        elif command.lower() == 'assign user project':
            username = input('Enter user name: ')
            projectname = input('Enter project name: ')
            print("Role Options")
            print("1. Owner")
            print("2. Admin")
            print("3. Manager")
            print("4. Employee")
            roleID = int(input('Enter role (Option 1-4): '))
            assign_user_project(username, projectname, roleID)
        
        elif command.lower() == 'assign user group':
            username = input('Enter user name: ')
            groupname = input('Enter group name: ')
            assign_user_group(username, groupname)
        
        elif command.lower() == 'assign group project':
            groupname = input('Enter group name: ')
            projectname = input('Enter project name: ')
            print("Role Options")
            print("1. Owner")
            print("2. Admin")
            print("3. Manager")
            print("4. Employee")
            roleID = int(input('Enter role (Option 1-4): '))
            assign_group_project(groupname, projectname, roleID)
        
        elif command.lower() == 'show user':
            username = input('Enter user name: ')
            show_user(username)
        
        elif command.lower() == 'show project':
            projectname = input('Enter project name: ')
            show_project(projectname)
        
        elif command.lower() == 'show group':
            groupname = input('Enter group name: ')
            show_group(groupname)
        
        elif command.lower() == 'show all users':
            show_all_users()
        
        elif command.lower() == 'show all projects':
            show_all_projects()
        
        elif command.lower() == 'show all groups':
            show_all_groups()
        
        elif command.lower() == 'delete user':
            username = input('Enter user name: ')
            delete_user(username)
        
        elif command.lower() == 'delete project':
            projectname = input('Enter project name: ')
            delete_project(projectname)
        
        elif command.lower() == 'delete group':
            groupname = input('Enter group name: ')
            delete_group(groupname)
        
        elif command.lower() == 'unassign user project':
            username = input('Enter user name: ')
            projectname = input('Enter project name: ')
            unassign_user_project(username, projectname)
        
        elif command.lower() == 'unassign user group':
            username = input('Enter user name: ')
            groupname = input('Enter group name: ')
            unassign_user_group(username, groupname)
        
        elif command.lower() == 'unassign group project':
            groupname = input('Enter group name: ')
            projectname = input('Enter project name: ')
            unassign_group_project(groupname, projectname)
        
        elif command.lower() == 'change role':
            username = input('Enter user name: ')
            projectname = input('Enter project name: ')
            print("Role Options")
            print("1. Owner")
            print("2. Admin")
            print("3. Manager")
            print("4. Employee")
            roleID = int(input('Enter role (Option 1-4): '))
            change_role(username, projectname, roleID)
        
        elif command.lower() == 'change role group':
            groupname = input('Enter group name: ')
            projectname = input('Enter project name: ')
            print("Role Options")
            print("1. Owner")
            print("2. Admin")
            print("3. Manager")
            print("4. Employee")
            roleID = int(input('Enter role (Option 1-4): '))
            change_role_group(groupname, projectname, roleID)
        
        else:
            print('Invalid command')

if __name__ == '__main__':
    try:
      main()
    except TypeError:
      print("Sorry! Some error occured, might be no data found.")
    except Exception as e:
      print(e)

