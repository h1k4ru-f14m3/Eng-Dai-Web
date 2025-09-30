let offset_gap = 25;

export async function search(query) {
    console.log(query);

    let response = await fetch(query);
    let results = await response.text();

    return results;
}


export function init_search(input, mode, output, sentinel) {
    input.addEventListener('input', async function () {
        let search_query = make_query(input.value,mode);
        let result = await search(search_query);
        let output_element = document.querySelector(output);
        
        output_element.innerHTML = result;

        const num_of_outputs = output_element.children.length - 1;
        console.log(num_of_outputs);
        if (num_of_outputs !== 0) {
            sentinel.innerHTML = "Loading...";
        }

        output_element.appendChild(sentinel);
        output_element.scrollTop = 0;
    })
}


export function make_query(input, mode, offset=0) {
    return '/search?m=' + mode + '&offset=' + offset + '&q=' + input;
}

// export function del_sentinel() {

// }

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
    let output_element = document.querySelector(output);


    const observer = new IntersectionObserver((entries) => {
        entries.forEach(async entry => {
            if (entry.isIntersecting) {
                let query = input.value;
                if (query !== current_query) {
                    offset_amt = 0;
                    current_query = query;
                }

                offset_amt += 25;

                let result = await search(make_query(query,mode,offset_amt));
                sentinel.insertAdjacentHTML('beforebegin', result);

                // Get the number of items in the whole list
                const num_of_items = output_element.children.length - 1;
                
                // Get the amount of how many items the API outputted
                let temp_div = document.createElement('div');
                temp_div.innerHTML = result;
                let response_elements_amt = temp_div.children.length;
                
                // Comment the following if u want
                console.log(`Items: ${num_of_items} ; Offset: ${offset_amt} ; Outputs: ${response_elements_amt}`);

                // Change the sentinel message 
                // if (offset_amt >= num_of_items) {
                //     sentinel.innerHTML = "";
                // } else if (response_elements_amt === 0 && num_of_items === 0) {
                //     sentinel.innerHTML = "No results :(";
                // } 
                // else {
                //     sentinel.innerHTML = "Loading...";
                // }
                if (response_elements_amt === 0) {
                    if (num_of_items === 0) {
                        sentinel.innerHTML = "No results :(";
                    }
                    else {
                        sentinel.innerHTML = "No more results.";
                    }
                } else {
                    sentinel.innerHTML = "Loading...";
                }
            }
        });
    }, {
        rootMargin: '100px'
    });

    observer.observe(sentinel);
}