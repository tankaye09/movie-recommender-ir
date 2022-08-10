# Usage

## Install virtual environment

`python -m venv .venv`

On git bash

`source .venv/Scripts/activate`

On other windows terminals

`.venv\Scripts\activate`

On mac

`source .venv/bin/activate`

## Install requirements

`pip3 install -r requirements.txt`

## Create directories and run ipynb files to generate pickle files

Create a pickle directory

## Build the web app

```
cd client
npm run build
```

## To run flask server

From root

`python -m flask run`
or
`FLASK_ENV=development flask run`

## To access webapp

Got to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

# Files

`app.py` contains the code for the flask application.

The preprocessing code is located in TFIDF Cosine Similarity.ipynb.
The code for the movies overview processing are located in the respective jupyter notebook files.
