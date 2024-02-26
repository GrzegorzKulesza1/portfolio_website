# My portfolio website

This is my personal website created in Python using the Flask framework. For the website style I mainly used Bootstrap.

The live version of the website can be viewed at: [www.grzegorz-kulesza.pl](https://www.grzegorz-kulesza.pl)

## Technologies Used
* **Flask:** The web framework used to build the application.
* **Jinja:** The templating engine integrated with Flask for dynamic content rendering.
* **Bootstrap:** Utilized for styling and creating a responsive design.
* **SQLAlchemy:** Used to interact with the database and manage data.
* **Requests:** Used to establish a connection with external API.
* **Random:** Used to create random sample from data and selecting random digits.
* **Time and DateTime:** Used for time-related functions.
* **Secrets:** Used for generating secure random strings.
* **os:** Used for environment variable management.

## Overview
I have posted several of my projects on the website, which you can find in the blueprints' folder.

#### Amber
![Amber Image](/static/images/amber_img.jpg)

The program evaluates whether the wind conditions are favorable for the sea to washed up amber onto the beach. You can 
check the weather in various towns where amber is commonly found.

To fetch data, the program utilizes the `requests` library to establish a connection with the API provided by 
[meteomatics.com](https://www.meteomatics.com).

#### Quiz
![Quiz Image](/static/images/quiz_img.png)

Enables users to assess their knowledge across different categories. In the form, users have the option to choose 
the number of questions and select a category. After answering the questions, users can review their correct responses 
and view their overall score.

The form is constructed using the `flask_wtf` extension to Flask. Questions are retrieved from a file using the `csv` 
library and are randomly selected with the `random` library.

#### To-Do List
![To-Do List Image](/static/images/todo_img.png)

The program enables users to create to-do lists, allowing them to add, edit, delete, and mark tasks as completed. 
The application also supports saving and uploading to-do lists.

To distinguish between individual users, the program uses the Flask `session` extension. This enables multiple 
users to use the application simultaneously. Each time a user reopens the browser, a new session is created with 
default data.

The program uses a combination of temporary variables and a database to manage user data.
* Temporary data is stored in the `users` variable, facilitating the creation of task lists without the need for saving.
* The SQLAlchemy database is utilized for permanent storage of data when a user chooses to save their list.

#### Other things
On the website you will also find:
* Certificates of the courses I have completed.
* Section about me where you can find out who I am.
* My contact information.

