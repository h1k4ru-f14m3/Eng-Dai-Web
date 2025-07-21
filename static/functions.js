export function search(input,mode,output,external_function) {
    input.addEventListener('input', async function() {
        let response = await fetch('/search?m=' + mode + '&q=' + input.value);
        let results = await response.text();
        
        document.querySelector(output).innerHTML = results;
        document.querySelector(output).scrollTo = 0;

        external_function();
    });
}

export function addListeners() {
    let buttons = document.querySelectorAll('.admininput');
    let modal = document.querySelector('.modal');
    let cancel = document.querySelector('.buttons #cancel');

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            modal.style.visibility = 'visible';
            let wordid = this.dataset.id;
            let eng = this.dataset.eng;
            let dai = this.dataset.dai;

            document.querySelector('.id-input').value = wordid;
            document.querySelector('.eng-input').value = eng;
            document.querySelector('.dai-input').value = dai;
                
            console.log(wordid);
        });
    });

    cancel.addEventListener("click", function() {
        modal.style.visibility = 'hidden';
        console.log('close!');
    });
}