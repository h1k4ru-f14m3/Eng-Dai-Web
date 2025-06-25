function search(input,mode,output) {
    input.addEventListener('input', async function() {
        let response = await fetch('/search?m=' + mode + '&q=' + input.value);
        let results = await response.text();
        
        document.querySelector(output).innerHTML = results;
        document.querySelector(output).scrollTo = 0;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // For index.html
    let index_input = document.querySelector("#index_search");
    search(index_input,'normal','#index_list');

    // For admin.html
    let admin_input = document.querySelector("#admin_search");
    search(admin_input,'admin','#admin_list');

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
            console.log('okay!');
        });
    });

    cancel.addEventListener("click", function() {
        modal.style.visibility = 'hidden';
        console.log('close!')
    });
})