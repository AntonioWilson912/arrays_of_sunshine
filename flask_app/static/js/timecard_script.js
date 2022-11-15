var createTimecardForm = document.getElementById("createTimecardForm");
var updateTimecardForm = document.getElementById("updateTimecardForm");

createTimecardForm.onsubmit = function(e) {
    e.preventDefault();
    var form = new FormData(createTimecardForm);
    fetch("http://localhost:5000/timecards/create", { "method": "POST", body: form })
        .then(res => res.json())
        .then(data => {

        })
}

updateTimecardForm.onsubmit = function(e) {
    e.preventDefault();
    var form = new FormData(updateTimecardForm)
    fetch("http://localhost:5000/timecards/update", { "method": "POST", body: form })
        .then(res => res.json())
        .then(data => {

        });
}

function createTimecard() {

}

function updateTimecard() {

}

function addBreak() {

}