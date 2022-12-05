var updateTimecardForm = document.getElementById("updateTimecardForm");

createTimecardForm.onsubmit = function(e) {
    e.preventDefault();
    var form = new FormData(createTimecardForm);
    console.log(form);
    //fetch("http://localhost:5000/team/3/timecards/create", { "method": "POST", body: form })
        // .then(res => res.json())
        // .then(data => {
        //     console.log(data);
        // });
}

updateTimecardForm.onsubmit = function(e) {
    e.preventDefault();
    var form = new FormData(updateTimecardForm)
    fetch("http://localhost:5000/timecards/update", { "method": "POST", body: form })
        .then(res => res.json())
        .then(data => {

        });
}

function updateTimecard() {

}

function addBreak() {
    console.log("Button clicked");
    var breakTemplate = `
    <div class="col">
        <label class="control-label">Break ${breakIndex}:</label>
    </div>
    <div class="col">
        <div class="row">
            <div class="col">
                <input class="form-control" id="breakStart${breakIndex}" name="breakStart${breakIndex}" type="time">
            </div>
            <div class="col">
                <input class="form-control" id="breakEnd${breakIndex}" name="breakEnd${breakIndex}" type="time">
            </div>
        </div>
    </div>
    `;
    var newBreak = document.createElement("div");
    newBreak.classList.add("row");
    newBreak.innerHTML = breakTemplate;
    document.getElementById("breakContainer").appendChild(newBreak);
    breakIndex++;
}