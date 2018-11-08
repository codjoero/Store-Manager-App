# Store-Manager-App

[![Build Status](https://travis-ci.org/codjoero/Userprofile.svg?branch=develop)](https://travis-ci.org/codjoero/Userprofile)
[![Coverage Status](https://coveralls.io/repos/github/codjoero/Store-Manager-App/badge.svg?branch=develop)](https://coveralls.io/github/codjoero/Store-Manager-App?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/1cc0ea9fdebf640c8169/maintainability)](https://codeclimate.com/github/codjoero/Store-Manager-App/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6cc05ba8faff4376bcbf48bd0645c1c2)](https://www.codacy.com/app/codjoero/Store-Manager-App?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codjoero/Store-Manager-App&amp;utm_campaign=Badge_Grade)

## About

Store Manager is a web application that helps Store-owners manage sales, product inventory records and staff.
It also allows staff allocated authority by the Store-owner, to login and start Shopping Carts for customers, interract with the product inventory and make sale records that can be viewed by the owner wherever they are.

### Dev Setup

To get the project, clone it using [Github Repo](https://github.com/codjoero/Store-Manager-App). Also the current work in progress App is on [github pages](https://codjoero.github.io/Store-Manager-App/)

This is app is hosted on [heroku](https://thecodestoremanager-api-heroku.herokuapp.com/).

# Heroku Endpoints

| Functionality | HTTP Method | Endpoint    | 
|---------------|:-----------:|------------:|
| index / welcome |     | / |
| new account | POST | /api/v1/user |
| update account | PUT | /api/v1/user/id |
| delete account | DELETE | /api/v1/user/id |
| add new product | POST | /api/v1/products |
| modify product | PUT | /api/v1/products/id |
| delete product | DELETE | /api/v1/products/id |
| add a sale order | POST | /api/v1/sales |
| view a sale order | GET | /api/v1/sales/id |
| view all sale records | GET | /api/v1/sales |

### Documentation

The documentation can be found [here](https://documenter.getpostman.com/view/5459960/RWgxvFDm)

### Prerequisites

    Web browser
    Internet

[gh-pages](https://codjoero.github.io/Store-Manager-App/)

### Installation

* Clone project to your local machine
* Current updated branch - features.

### Tests
#### Pending....

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
To all developers at [Andela](https://andela.com) I salute thee. And to all that have made this development process possible, you're heros to me.

#### License
Andela Opensource