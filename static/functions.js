let offset_gap = 25;

export async function search(query) {
    let response = await fetch(query);
    let results = await response.text();

    return results;
}


export function init_search(input, mode, output, sentinel) {
    input.addEventListener('input', async function () {
        let search_query = make_query(input.value,mode);
        let result = await search(search_query);

        document.querySelector(output).innerHTML = result;
        document.querySelector(output).appendChild(sentinel);
        document.querySelector(output).scrollTop = 0;
    })
}


export function make_query(input, mode, offset=0) {
    return '/search?m=' + mode + '&offset=' + offset + '&q=' + input;
}

export function addModal(button, modal_selector, cancel_selector, selectors, header="Edit Panel") {
    let buttons = document.querySelectorAll(button);
    let modal = document.querySelector(modal_selector);
    let cancel = document.querySelector(cancel_selector);

    buttons.forEach(function (button) {
        button.addEventListener("click", function() {
            modal.style.visibility = 'visible';
            let values = Object.values(this.dataset);
            modal.querySelector('h1').innerHTML = header;
            
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


export function init_observer (input,mode,output,sentinel) {
    let offset_amt = 0;
    let current_query = '';


    const observer = new IntersectionObserver((entries) => {
        entries.forEach(async entry => {
            if (entry.isIntersecting) {
                let query = input.value;
                if (query !== current_query) {
                    offset_amt = 0;
                    current_query = query;
                }

                offset_amt += 25;
                console.log(make_query(query,mode,offset_amt));
                let result = await search(make_query(query,mode,offset_amt));
                sentinel.insertAdjacentHTML('beforebegin', result);
            }
        });
    }, {
        rootMargin: '100px'
    });

    observer.observe(sentinel);
}