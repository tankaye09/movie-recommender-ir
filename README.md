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
