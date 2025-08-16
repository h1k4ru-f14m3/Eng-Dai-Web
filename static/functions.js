export function search(input,mode,output,external_function) {
    input.addEventListener('input', async function() {
        let response = await fetch('/search?m=' + mode + '&q=' + input.value);
        let results = await response.text();
        
        document.querySelector(output).innerHTML = results;
        document.querySelector(output).scrollTo = 0;

        external_function();
    });
}


export function addModal(button, modal_selector, cancel_selector, selectors) {
    let buttons = document.querySelectorAll(button);
    let modal = document.querySelector(modal_selector);
    let cancel = document.querySelector(cancel_selector);

    buttons.forEach(function (button) {
        button.addEventListener("click", function() {
            modal.style.visibility = 'visible';
            let values = Object.values(this.dataset);
            
            set_values(selectors, values);
        });
    });

    cancel.addEventListener("click", function() {
        modal.style.visibility = 'hidden';
        console.log('close!');
    });
}


export function set_values(selectors,values) {
    selectors.forEach(function (selector, i) {
        document.querySelector(selector).value = values[i];
    });
}


export function runFlaskRoute(queryToRun, formSelector, messageSelector) {
    const form = document.querySelector(formSelector);
    const message = document.querySelector(messageSelector);

    fetch(queryToRun, {
        method: "POST",
        body: new FormData(form),
    }).then(result => result.text()).then(
        data => {
            if (data.trim() === "success"){
                window.location.replace("/");
            }
            else {
                message.style.visibility = 'visible';
                message.innerHTML = data;
            }
        }
    );
}


export function listenEnter(formSelector, buttonSelector) {
    const form = document.querySelector(formSelector);
    const btn = document.querySelector(buttonSelector);

    form.addEventListener("keypress", function(event){
        if (event.key === "Enter") {
            event.preventDefault();
            btn.click();
        }
    })
}