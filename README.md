# Django JWT Template Project

This backend template is built to be paired and implemented with the [React_JWT_Template project](https://github.com/Rasky26/React_JWT_Template)

<hr />

Recommended to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to contain all the libraries used with this project.

> Within the main project folder, run the terminal commands to create a virtual environment folder and scripts.
> ```
> python3 -m venv venv
>
>   (on Windows)
> source venv/Scripts/activate
> ```
> Check the docs for Apple/Unix systems

<hr />

Once the template is cloned and the virtual environment is activated, then:
> Install the required libraries from the `requirements.txt` file with the following command line in the terminal
> ```
> pip install -r /path/to/requirements.txt
> ```
> If done correctly, all the library files will reside in the `venv/Lib` file

<hr />

Once the installation is complete, navigate to the `core/` folder in the terminal that contains the file `manage.py`.

> Run the following commands in the terminal to build your basic starting database:
> ```
> python manage.py makemigrations
> ```
> ^^This command stages all the database information (or changes), but does not create or modify your database
> ```
> python manage.py migrate
> ```
> ^^This command takes the staged information and creates / modifies your database

<hr />

At this point, you can launch the server and make all the existing routes available to access via [http://localhost:8000/](http://localhost:8000/). This is the root URL that other routes are built on (such as http://localhost:8000/accounts)
> Run the following command to launch your Django server:
> ```
> python manage.py runserver
> ```
> The built-in Django admin page can be accessed via: [http://localhost:8000/admin/](http://localhost:8000/admin/).
> In order to access the admin page, you will need to create a `superuser` using the following command in the terminal:
> ```
> python manage.py createsuperuser
> ```
> Once those fields are filled out, you can successfully log into the admin page.
