

<!-- PROJECT HEADER/LOGO -->
<!-- <br /> -->

<p align="center">
  <!--
  <a href="https://github.com/abassel/Flask-RestGlue">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  -->
  <h1 align="center">Flask-RestGlue(ALPHA)</h1>

  <p align="center">
    Integrates <b>Flask + MongoDB + OpenAPI</b> in a simple and elegant way!
    <br />
    <a href="https://abassel.github.io/Flask-RestGlue/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/abassel/Flask-RestGlue#example">View Demo</a>
    ·
    <a href="https://github.com/abassel/Flask-RestGlue/issues">Report Bug</a>
    ·
    <a href="https://github.com/abassel/Flask-RestGlue/issues">Request Feature</a>
  </p>

  <p align="center">
      <a href="https://github.com/abassel/Flask-RestGlue/actions?query=workflow%3Abuild"><img src="https://github.com/abassel/Flask-RestGlue/workflows/build/badge.svg?branch=master&event=push" alt="Stars Badge"/></a>
      <a href="https://github.com/abassel/Flask-RestGlue/pulls"><img src="https://img.shields.io/github/issues-pr/abassel/Flask-RestGlue" alt="Pull Requests Badge"/></a>
      <a href="https://github.com/abassel/Flask-RestGlue/issues"><img src="https://img.shields.io/github/issues/abassel/Flask-RestGlue" alt="Issues Badge"/></a>
  </p>

  <p align="center">
   <a href="https://pypi.org/project/Flask-RestGlue/"><img src="https://img.shields.io/pypi/pyversions/Flask-RestGlue.svg" alt="Python Version"/></a>
   <a href="https://github.com/abassel/Flask-RestGlue/releases"><img src="https://img.shields.io/pypi/v/Flask-RestGlue?color=green&label=version" alt="Version"/></a>
   <a href="https://github.com/abassel/Flask-RestGlue/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot"><img src="https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg" alt="Dependencies Status"/></a>
   <a href="https://github.com/PyCQA/bandit"><img src="https://img.shields.io/badge/security-bandit-green.svg" alt="Security: bandit"/></a>
   <a href="https://github.com/abassel/Flask-RestGlue/blob/master/.pre-commit-config.yaml"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="Pre-commit"/></a>
   <a href="https://github.com/abassel/Flask-RestGlue/blob/master/LICENSE"><img src="https://img.shields.io/github/license/abassel/Flask-RestGlue" alt="License"/></a>
  </p></p>


<!-- TABLE OF CONTENTS -->
## Contents
<details>
  <summary>Table of Contents</summary>
  <ol>
    <!--
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    -->
    <li><a href="#example">Example</a></li>
    <li><a href="#quick-start">Quick Start</a></li>
    <li><a href="#references-notebook">References</a></li>
    <!--<li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>-->
  </ol>
</details>



# Example

For a fullstack boilerplate, visit [https://github.com/abassel/Flask_RestGlue_Svelte_Docker](https://github.com/abassel/Flask_RestGlue_Svelte_Docker)

```python
import mongoengine as mongo
from flask_rest_glue import FlaskRestGlue

mongo.connect("pyglue", host='localhost:27017')

api = FlaskRestGlue()


@api.rest_model()
class User(mongo.Document):
  # id = mongo.StringField(primary_key=True)
  email = mongo.StringField(primary_key=True)
  password = mongo.StringField()


api.run()

```

Go to [http://127.0.0.1:5000/spec_doc](http://127.0.0.1:5000/spec_doc) or [http://127.0.0.1:5000/spec_rdoc](http://127.0.0.1:5000/spec_rdoc) to see the documentation bellow:

![Swagger UI](https://abassel.github.io/Flask-RestGlue/swagger.png)

![ReText UI](https://abassel.github.io/Flask-RestGlue/rdoc.png)

### Expected output:

```bash
curl -v -d '{"email":"a@b.com","password":"xyz"}' \
     -H "Content-Type: application/json" http://localhost:5000/user

#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 45
#<
#{
#  "_id": "a@b.com",
#  "password": "xyz"
#}


curl -v http://localhost:5000/users
#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 57
#<
#[
#  {
#    "_id": "a@b.com",
#    "password": "xyz"
#  }
#]


curl -v http://localhost:5000/user/a@b.com
#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 45
#<
#{
#  "_id": "a@b.com",
#  "password": "xyz"
#}


curl -v -X PUT -d '{"password":"new_pass"}' \
     -H "Content-Type: application/json" http://localhost:5000/user/a@b.com
#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 50
#<
#{
#  "_id": "a@b.com",
#  "password": "new_pass"
#}


curl -v -X DELETE http://localhost:5000/user/a@b.com
#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 45
#<
#{
#  "_id": "a@b.com",
#  "password": "xyz"
#}
```


# Quick Start

Requires **docker** and **python 3.9**

### 1 - install local MongoDB
```bash
mkdir -p ~/mongodata

docker run -d --rm -p 27017:27017 -v ~/mongodata:/data/db --name mongodb mongo
```

### 2 - Install this library
```bash
pip install Flask-RestGlue
```

### 3 - Pull the code
```bash
curl -s -O -L  https://github.com/abassel/Flask-RestGlue/blob/master/example/tut01_hello_world.py
curl -s -O -L  https://github.com/abassel/Flask-RestGlue/blob/master/example/tut01_hello_world.sh
```

### 4 - Run the code
```bash
python tut01_hello_world.py
```
In another terminal window

```bash
bash tut01_hello_world.sh
```

## References :notebook:
- [Flask_RestGlue_Svelte_Docker boilerplate](https://github.com/abassel/Flask_RestGlue_Svelte_Docker)
- [OpenAPI 3.0.3](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md)
- [Flask](http://flask.pocoo.org)
- [Mongoengine](https://github.com/MongoEngine/mongoengine)
