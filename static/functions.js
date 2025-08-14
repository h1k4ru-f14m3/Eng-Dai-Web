export function search(input,mode,output,external_function) {
    input.addEventListener('input', async function() {
        let response = await fetch('/search?m=' + mode + '&q=' + input.value);
        let results = await response.text();
        
        document.querySelector(output).innerHTML = results;
        document.querySelector(output).scrollTo = 0;

        external_function();
    });
}

export function addModal(button, modal_selector, cancel_selector, selectors, values) {
    let buttons = document.querySelectorAll(button);
    let modal = document.querySelector(modal_selector);
    let cancel = document.querySelector(cancel_selector);

    buttons.forEach(function (button) {
        button.addEventListener("click", function() {
            modal.style.visibility = 'visible';
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