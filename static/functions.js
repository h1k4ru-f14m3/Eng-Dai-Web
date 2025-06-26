export function search(input,mode,output,external_function) {
    input.addEventListener('input', async function() {
        let response = await fetch('/search?m=' + mode + '&q=' + input.value);
        let results = await response.text();
        
        document.querySelector(output).innerHTML = results;
        document.querySelector(output).scrollTo = 0;

        external_function();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // For index.html
    let index_input = document.querySelector("#index_search");
    search(index_input,'normal','#index_list');
});