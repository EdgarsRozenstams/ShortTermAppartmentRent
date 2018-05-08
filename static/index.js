// Get modal element

var modal = document.getElementById('simpleModal');
//get modal btn
var modalBtn = document.getElementById('rent');
//get close btn
var closeBtn = document.getElementsByClassName('closeBtn')[0];

//listen for open click
modalBtn.addEventListener('click', openModal);

//listen for close click
closeBtn.addEventListener('click', closeModal);

//listen for outside click

window.addEventListener('click', clickOutside)


//function to open modal
function openModal() {
    modal.style.display = 'block';
}

//function to close
function closeModal() {
    console.log(456);
    modal.style.display = 'none';
}


//function to close modal is outise click
function clickOutside(e) {
   if (e.target == modal){

       modal.style.display = 'none';

   }
}