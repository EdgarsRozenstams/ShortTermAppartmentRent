var modal = document.getElementById('simpleModal');
var modalBtn = document.getElementById('rent');
var closeBtn = document.getElementsByClassName('closeBtn')[0];

modalBtn.addEventListener('click', openModal);
closeBtn.addEventListener('click', closeModal);
window.addEventListener('click', clickOutside)

function openModal() {
    modal.style.display = 'block';
}

function closeModal() {
    console.log(456);
    modal.style.display = 'none';
}

function clickOutside(e) {
    if (e.target == modal){
        modal.style.display = 'none';
    }
}

//credit: https://www.youtube.com/watch?v=6ophW7Ask_0&t=1567s