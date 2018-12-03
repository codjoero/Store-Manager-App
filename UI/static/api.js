class Api {
    constructor() {
        this.url = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/';
        this.token = localStorage.getItem('token');
        this.loggedUser = localStorage.getItem('loggedUser');

    }

    post(endpoint, data) {
        const resp = fetch(this.url + endpoint, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-type': 'application/json',
                'Authorization': 'Bearer '+ this.token 
            },
            body:JSON.stringify(data)
        });
        return resp;
    }

    put(endpoint, data) {
        const resp = fetch(this.url + endpoint, {
            method: 'PUT',
            mode: 'cors',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-type': 'application/json',
                'Authorization': 'Bearer '+ this.token 
            },
            body:JSON.stringify(data)
        });
        return resp;
    }

    get(endpoint) {
        const resp = fetch(this.url + endpoint, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-type': 'application/json',
                'Authorization': 'Bearer '+ this.token 
            },
        });
        return resp;
    }

    delete(endpoint) {
        const resp = fetch(this.url + endpoint, {
            method: 'DELETE',
            mode: 'cors',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Authorization': 'Bearer '+ this.token
            }
        });
        return resp;
    }

    //Handle response
    handleResponse(response) {
        return response.json()
        .then(json => {
            if (response.ok) {
                return json;
            } else {
                return Promise.reject(json);
            }
        });
    }

    style() {
        let paragraph = document.querySelector('span.loggedin');
        paragraph.innerHTML += this.loggedUser;
    }

    //Clear all table rows
    clearTable(tableBody) {
        while (tableBody.firstChild) {
            tableBody.removeChild(tableBody.firstChild);
        }
    }

    shortDate(date) {
        var length = 16;
        return date.substring(0, length);
    }

    errCheck(err) {
        if (err['msg'] === 'Token has expired' ||
            err['message'] === 'Invalid Authentication, Please Login!' ||
            err['message'] === 'Unauthorized Access!') {
            window.location = '/UI/templates/index.html';
        }
    }
}