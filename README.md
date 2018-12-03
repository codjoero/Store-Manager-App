# Store-Manager-App

[![Build Status](https://travis-ci.org/codjoero/Store-Manager-App.svg?branch=develop)](https://travis-ci.org/codjoero/Store-Manager-App)
[![Coverage Status](https://coveralls.io/repos/github/codjoero/Store-Manager-App/badge.svg?branch=develop)](https://coveralls.io/github/codjoero/Store-Manager-App?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/1cc0ea9fdebf640c8169/maintainability)](https://codeclimate.com/github/codjoero/Store-Manager-App/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6cc05ba8faff4376bcbf48bd0645c1c2)](https://www.codacy.com/app/codjoero/Store-Manager-App?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codjoero/Store-Manager-App&amp;utm_campaign=Badge_Grade)

## About

Store Manager is a web application that helps Store-owners manage sales, product inventory records and staff.
It also allows staff allocated authority by the Store-owner, to login and start Shopping Carts for customers, interract with the product inventory and make sale records that can be viewed by the owner wherever they are.

### Dev Setup

To get the project, clone it using [Github Repo](https://github.com/codjoero/Store-Manager-App). Also the current App is on [github pages](https://codjoero.github.io/Store-Manager-App/)

This is app is hosted on [heroku](https://thecodestoremanager-api-heroku.herokuapp.com/).

## Heroku Endpoints

| Functionality | HTTP Method | Endpoint    | 
|---------------|:-----------:|------------:|
| `index / welcome` |     | / |
| `new account` | POST | /api/v1/user |
| `update account` | PUT | /api/v1/user/id |
| `delete account` | DELETE | /api/v1/user/id |
| `add new product` | POST | /api/v1/products |
| `modify product` | PUT | /api/v1/products/id |
| `delete product` | DELETE | /api/v1/products/id |
| `add a sale order` | POST | /api/v1/sales |
| `view a sale order` | GET | /api/v1/sales/id |
| `view all sale records` | GET | /api/v1/sales |

## Functionality

| Function | Access |
| ------------- | ------------- |
|`Admin registeration` | admin |
|`User login` | store attendant and admin |
|`Add accounts for store attendants` | admin |
|`Add products` | admin |
|`Update store attendant's accounts`| admin |
|`Delete store attendant's accounts` | admin |
|`Update products` | admin |
|`Delete product` | admin |
|`View all products` | store attendant and admin |
|`Add sale records` | store attendant |
|`View all users' sale records` | admin |
|`View a store attendant sale records` | store attendant and admin |

### Documentation

The documentation can be found [here](https://documenter.getpostman.com/view/5459960/RWgxvFDm)

### Prerequisites

    Web browser
    Internet

[gh-pages](https://codjoero.github.io/Store-Manager-App/)
### Note
- admin can be registered only if non exists
- Current admin:
```sh
   username: jonnie
   password: Andela8
```

### Installation

* Clone project to your local machine
```sh
  $ git clone https://github.com/codjoero/Store-Manager-App.git
  ```
* Run through the following settings
```sh
    $ cd Store-Manager-App
    $ pip install virtualenv
    $ virtualenv env
    $ . env/bin/activate (windows: $ source env/Scripts/activate)
    $ pip install -r requirements.txt
    $ python3 run.py
```

### Tests
```sh
   $ . env/bin/activate (windows: $ source env/Scripts/activate)
   $ pip install pytest
   $ python3 -m pytest
```

### Tech used 
App built with the following tech:-
   * HTML5 
   * CSS3
   * Javascript
   * Python/Flask
   * Virtualenv

### To contribute to this App
Create a branch from **feature**, make a PR and I will review and merge if possible.
### Author
Ronald Nsereko
### Acknowledgements
Thanks to the developers at [Andela](https://andela.com). And to all that have made this development process possible, you're heros to me.

#### License
Andela Opensource