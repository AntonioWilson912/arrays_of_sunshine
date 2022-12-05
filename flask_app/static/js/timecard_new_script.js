var createTimecardForm = document.getElementById("createTimecardForm");
var breakIndex = 1;

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

function createTimecard() {

}

function addBreak() {
    console.log("Button clicked");
    var breakTemplate = `
    <div class="col">
        <ul id="breakErrors${breakIndex}"></ul>
        <div class="row">
            <div class="col">
                <label class="control-label" id="breakLabel${breakIndex}">Break ${breakIndex}:</label>
            </div>
            <div class="col">
                <div class="row">
                    <div class="col">
                        <input class="form-control" id="breakStart${breakIndex}" name="breakStart${breakIndex}" type="time" onfocusout="validateBreak(this);">
                    </div>
                    <div class="col">
                        <input class="form-control" id="breakEnd${breakIndex}" name="breakEnd${breakIndex}" type="time" onfocusout="validateBreak(this);">
                    </div>
                    <div class="col">
                        <i class="text-danger fa-solid fa-circle-xmark" id="removeBreak${breakIndex}" style="font-size: 2rem;" onclick="removeBreak(${breakIndex});"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;
    var newBreak = document.createElement("div");
    newBreak.id = "break" + breakIndex;
    newBreak.classList.add("row");
    newBreak.innerHTML = breakTemplate;
    document.getElementById("breakContainer").appendChild(newBreak);
    breakIndex++;
}

function validateBreak(element) {
    let breakStart, breakEnd, breakErrors, breakNum;

    // Check if this is the break start or the break end
    if (element.id.toLowerCase().includes("start")) {
        breakNum = element.id.slice(10);
        breakStart = element;
        breakEnd = document.getElementById("breakEnd" + breakNum);
        breakErrors = document.getElementById("breakErrors" + breakNum);
    }
    else {
        breakNum = element.id.slice(8);
        breakStart = document.getElementById("breakStart" + breakNum);
        breakEnd = element;
        breakErrors = document.getElementById("breakErrors" + breakNum);
    }

    breakErrors = document.getElementById("breakErrors" + breakNum);
    breakErrors.innerHTML = "";
    console.log("Break", breakNum, ":", breakStart.value + " - " + breakEnd.value);
    if (breakStart.value != "" && breakStart > breakEnd.value) {
        var error = document.createElement("li");
        error.classList.add("text-danger");
        error.innerText = "Break start must be less than break end.";
        breakErrors.appendChild(error);
    }
}

function removeBreak(breakIndexToRemove) {
    var breakToRemove = document.getElementById("break" + breakIndexToRemove);
    console.log("Searching for break #" + breakIndexToRemove);
    if (!breakToRemove) {
        console.log("Yikes");
        return;
    }

    breakToRemove.remove();

    // Now fill the gap
    for (var index = breakIndexToRemove; index < breakIndex; index++) {
        // Get the break container, label, start, end, error, and remove elements
        if (document.getElementById("break" + (index + 1))) {
            var breakContainer = document.getElementById("break" + (index + 1));
            var breakLabel = document.getElementById("breakLabel" + (index + 1));
            var breakStart = document.getElementById("breakStart" + (index + 1));
            var breakEnd = document.getElementById("breakEnd" + (index + 1));
            var breakErrors = document.getElementById("breakErrors" + (index + 1));
            var breakRemove = document.getElementById("removeBreak" + (index + 1));
    
            breakContainer.id = "break" + index;
            breakLabel.id = "breakLabel" + index;
            breakLabel.innerText = `Break ${index}:`;
            breakStart.id = "breakStart" + index;
            breakEnd.id = "breakEnd" + index;
            breakErrors.id = "breakErrors" + index;

            // Create a new remove break button for the onclick event to work properly
            breakRemove.id = "removeBreak" + index;
            breakRemove.removeEventListener("onclick");
            breakRemove.addEventListener("onclick", removeBreak(index));
        }
    }
    console.log("Break index before:", breakIndex);
    breakIndex--;
    console.log("Break index after:", breakIndex);
}