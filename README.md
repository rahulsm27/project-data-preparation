# project_template
project environment setup template


MAKEFILE
makefile can make running repetitive commdns easier

Poetry
Dependency resolution and locking of external libraries.

#Code formatting - Black
formats code to make it easier to read as per predefined standards

#imports soritng - isort
sorts import alphabetically and types


#linting -  flake8
check python codebase for errors stlying issues and complexity baesd upon 3 tools
pyflakes mccabe and pycodestyle

#type checking- mypy
# run mppy ./<package name>  -> gives list of incompatibble types passed to argumens
#statigng  type check for python

----------------X------------------------------------X----
1 MAKEFILE


By default, Makefile targets are "file targets" - they are used to build files from other files. 857

Let's assume you have install target, which is a very common in makefiles. If you do not use .PHONY, and a file named install exists in the same directory as the Makefile, then make install will do nothing. This is because Make interprets the rule to mean "execute such-and-such recipe to create the file named install". Since the file is already there, and its dependencies didn't change, nothing will be done.

However if you make the install target PHONY, it will tell the make tool that the target is fictional, and that make should not expect it to create the actual file. Hence it will not check whether the install file exists, meaning: a) its behavior will not be altered if the file does exist and b) extra stat() will not be called.

Generally all targets in your Makefile which do not produce an output file with the same name as the target name should be PHONY. This typically includes all, install, clean, distclean, and so on.

MACRO_NAME  = MACRO_VALUE

.PHONY : target # phony if the target are not files
target:target-dependencies
    system command(s)
    @echo $(MACRO_VALUE)  # @ to avoid printing


----------------X------------------------------------X----
2 POETRY
Depenency resolved. Final version stored in lock file
Create dependency grops and install packages within a specific dependency group..for test create one depenency group and for prodcution another.

# in command line run below coammdn to create pyproject.toml file 
1. poetry init 

2. specify dependenceis in pyporject.toml file
3. poetry install 
# use command to install dependencies. It will automatically create a venv and install
Poetry makes project environment isolation one of its core features.

What this means is that it will always work isolated from your global Python installation. To achieve this, it will first check if it’s currently running inside a virtual environment. If it is, it will use it directly without creating a new one. But if it’s not, it will use one that it has already created or create a brand new one for you.

By default, Poetry will try to use the Python version used during Poetry’s installation to create the virtual environment for the current project.

4. poetry shell

# poetry shell provides a shorthand to activate the virtual environment. By default Poetry doesn't create the venv within the project folder, but in {cache-dir}/virtualenvs . So using the activate script would require to find out the location of the venv everytime you want to activate it.

5. poetry update
# to update any new dependencies in lock file

6. poetry install --only main --syn
# command to update only main dependencies and not test

<!-- Poetry install
Creates a poetry.lock file. This file is automatically updated when poetry add is run to install new dependencies, poetry update is run to update dependency versions, or poetry lock is run to check for conflicts.
Poetry update
Fetches the latest matching versions for dependencies and updates the lock file with the new versions. This is similar to deleting the poetry.lock file and running poetry install again. -->

#f there is already a poetry.lock file as well as a pyproject.toml file when you run poetry install, it means either you ran the install command before, or someone else on the project ran the install command and committed the poetry.lock file to the project (which is good).

Either way, running install when a poetry.lock file is present resolves and installs all dependencies that you listed in pyproject.toml, but Poetry uses the exact versions listed in poetry.lock to ensure that the package versions are consistent for everyone working on your project. As a result you will have all dependencies requested by your pyproject.toml file, but they may not all be at the very latest available versions (some dependencies listed in the poetry.lock file may have released newer versions since the file was created). This is by design, it ensures that your project does not break because of unexpected changes in dependencies.

The --sync can be combined with group-related options:

#dev docs are groups
poetry install --without dev --sync
poetry install --with docs --sync
poetry install --only dev

----------------X------------------------------------X----
# CODE FORMATING
Black - formats code as per pre defined standards 
black ./src

# IMPORTS SORING
ISORT - sort imports aplphabetcially and seperate into secitons and by type
isort ./src


# LINTING
FLAKE8 - linting toll that checks python codebase for errors styling issues
Doesn't support pyproject.toml. need to setup.cfg
flake8 ./src

# TYPE CHECKING
MYPY - type checks help ensure that we are usign variables and functions in code correctly
# cli
mypy ./src

----------------X------------------------------------X----
DOCKER COMPOSE
Docker Compose is a tool for running multi-container applications on Docker defined using the Compose file format. A Compose file is used to define how one or more containers that make up your application are configured. Once you have a Compose file, you can create and start your application with a single command: docker compose up.



----------------X------------------------------------X-----
---------------X------------------------------------X-------
-------------X------------------------------------X--------------------X------------------------------------X--------------------X------------------------------------X----