var registerEmployeeForm = document.getElementById("registerEmployeeForm");
var loginEmployeeForm = document.getElementById("loginEmployeeForm");
var createEmployeeForm = document.getElementById("createEmployeeForm");
var updateEmployeeForm = document.getElementById("updateEmployeeForm");

registerEmployeeForm.onsubmit = function(e) {
    e.preventDefault();
    var form = new FormData(registerEmployeeForm);
    fetch("http://localhost:5000/register_employee", { "method": "POST", body: form })
        .then(res => res.json())
        .then(data => {

        });
}

loginEmployeeForm.onsubmit = function(e) {
    e.preventDefault();
    var form = new FormData(loginEmployeeForm);
    fetch("http://localhost:5000/login_employee", { "method": "POST", body: form })
        .then(res => res.json())
        .then(data => {
            
        });
}

createEmployeeForm.onsubmit = function(e) {
    e.preventDefault();
    var form = new FormData(createEmployeeForm);
    fetch("http://localhost:5000/create_employee", { "method": "POST", body: form })
        .then(res => res.json())
        .then(data => {
            
        });
}

updateEmployeeForm.onsubmit = function(e) {
    e.preventDefault();
    var form = new FormData(updateEmployeeForm);
    fetch("http://localhost:5000/update_employee", { "method": "POST", body: form })
        .then(res => res.json())
        .then(data => {
            
        });
}