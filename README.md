# BurgerQueen

School project letting us explore connectivity between python and databases. Simple burger-ordering roleplay!🍔🍟
PS: The employee code to play as an employee is **NOAHBURGERS**

This project uses **SQLite**, which means the database is a local file (`BQv2.db`) created on your computer.

## How to install

### Get the project

#### Option A: Clone with Git

```
use this command to clone the repo:
$ git clone https://github.com/noah-dks/BurgerQueen.git

open the project directory
$ cd BurgerQueen
```

#### Option B: Download ZIP

1. Click the green Code button on GitHub and download ZIP
2. Extract the ZIP
3. Open a terminal in the extracted folder

### How to Run

#### Create a venv + install dependencies

1.  in the project directory, create a new venv and activate it:  
    **Windows:**
    ```
    create venv:
    $ python -m venv .venv

    activate venv:
    $ .venv\Scripts\Activate.ps1
     ```
    **Mac/Linux:**
    ```
    create venv:
    $ python3 -m venv .venv

    activate venv:
    $ source .venv/bin/activate
     ```
2.  Install Dependencies:   
 `pip install -r requirements.txt`


#### Create the database
You can easily create the database by running this script:   
`python createDB.py`

#### Run the program
In the terminal of project directory, simply run:  
`python main.py`

###  **PS: if you ever wanna run the project after closing it - ALWAYS remember to activate the venv before running!**

