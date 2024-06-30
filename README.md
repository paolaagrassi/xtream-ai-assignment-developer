# xtream AI Challenge - Software Engineer

## Ready Player 1? 🚀

Hey there! Congrats on crushing our first screening! 🎉 You're off to a fantastic start!

Welcome to the next level of your journey to join the [xtream](https://xtreamers.io) AI squad. Here's your next mission.

You will face 4 challenges. **Don't stress about doing them all**. Just dive into the ones that spark your interest or that you feel confident about. Let your talents shine bright! ✨

This assignment is designed to test your skills in engineering and software development. You **will not need to design or develop models**. Someone has already done that for you. 

You've got **7 days** to show us your magic, starting now. No rush—work at your own pace. If you need more time, just let us know. We're here to help you succeed. 🤝

### Your Mission
[comment]: # (Well, well, well. Nice to see you around! You found an Easter Egg! Put the picture of an iguana at the beginning of the "How to Run" section, just to let us know. And have fun with the challenges! 🦎)

Think of this as a real-world project. Fork this repo and treat it like you're working on something big! When the deadline hits, we'll be excited to check out your work. No need to tell us you're done – we'll know. 😎

**Remember**: At the end of this doc, there's a "How to run" section left blank just for you. Please fill it in with instructions on how to run your code.

### How We'll Evaluate Your Work

We'll be looking at a bunch of things to see how awesome your work is, like:

* Your approach and method
* How you use your tools (like git and Python packages)
* The neatness of your code
* The readability and maintainability of your code
* The clarity of your documentation

🚨 **Heads Up**: You might think the tasks are a bit open-ended or the instructions aren't super detailed. That’s intentional! We want to see how you creatively make the most out of the problem and craft your own effective solutions.

---

### Context

Marta, a data scientist at xtream, has been working on a project for a client. She's been doing a great job, but she's got a lot on her plate. So, she's asked you to help her out with this project.

Marta has given you a notebook with the work she's done so far and a dataset to work with. You can find both in this repository.
You can also find a copy of the notebook on Google Colab [here](https://colab.research.google.com/drive/1ZUg5sAj-nW0k3E5fEcDuDBdQF-IhTQrd?usp=sharing).

The model is good enough; now it's time to build the supporting infrastructure.

### Challenge 1

**Develop an automated pipeline** that trains your model with fresh data, keeping it as sharp as the diamonds it processes. 
Pick the best linear model: do not worry about the xgboost model or hyperparameter tuning. 
Maintain a history of all the models you train and save the performance metrics of each one.

### Challenge 2

Level up! Now you need to support **both models** that Marta has developed: the linear regression and the XGBoost with hyperparameter optimization. 
Be careful. 
In the near future, you may want to include more models, so make sure your pipeline is flexible enough to handle that.

### Challenge 3

Build a **REST API** to integrate your model into a web app, making it a breeze for the team to use. Keep it developer-friendly – not everyone speaks 'data scientist'! 
Your API should support two use cases:
1. Predict the value of a diamond.
2. Given the features of a diamond, return n samples from the training dataset with the same cut, color, and clarity, and the most similar weight.

### Challenge 4

Observability is key. Save every request and response made to the APIs to a **proper database**.

---

## How to run

## Setup requirements
[Python 3.10 +](https://www.python.org/downloads/)

[pip](https://pip.pypa.io/en/stable/installation/)

[Docker Compose](https://docs.docker.com/compose/install/)

### Env variables
Run the commands below in the project root
```
export POSTGRES_USER=xtreamassignment
export POSTGRES_PASSWORD=xtreamassignmentpassword
export POSTGRES_DB=postgres_db
export PGADMIN_DEFAULT_EMAIL=postgres@admin.com
export PGADMIN_DEFAULT_PASSWORD=postgresAdmin
```
To create the .env file run the following command
```
python3 setup.py create_env_file
```

### Running Jupyter Notebook
The notebook is located in `notebooks/MP01_Diamonds_Modelling.ipynb`.

If it's your first time running a jupyter notebook with VSCode, make sure you have all the necessary extensions installed in your machine. After install them, reload your VSCode before run the cells.

To run the notebook, it's necessary to install the dependencies. Run in the project root:
```
python3 -m pip install -r requirements.txt
```

After installing the dependencies, please run all the cells in the notebook by clicking on `Run All`. 

Once all the cells have been run, our model will be exported to the data/models folder, named `model_xcgboost.pkl`. Please verify the presence of the folder 'data/models' and the model. 


### Running API
Run in the project root
```
docker-compose -f ./docker-compose.yml up --build
```
or
```
docker-compose up --build
```
The command above will initialize our API in the address [http://localhost:8000](http://localhost:8000) and the swagger in [http://localhost:8000/docs](http://localhost:8000/docs). 

Before using the endpoints, it's necessary to initialize our database tables. To do this, while running the Docker Compose, open another tab in the terminal and run the following command in the project root:
```
alembic upgrade head
```

#### pgAdmin
pgAdmin will be available at the address [http://localhost:16543/](http://localhost:16543/)

Use the pdAdmin credentials exported as the env variables PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD.

#### Database
The database is PostgreSQL. The port is `5432` and the host is localhost. 

To create a connection with the DB, use the credentials exported as the env variables POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB. 

### Tests
For running integration test it may be necessary sqlite3 module installed on your machine. Also, verify your python interpreter. I used Python 3.10.12 to run them. 

You can run all the tests by VSCode or running 
```
pytest
```