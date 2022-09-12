var hamburger = document.querySelector('#ham')
var menu = document.querySelector('#menu')
var sideMenu = document.querySelector('#sideMenu')
var main_content = document.querySelector('#main_content')


window.onload=function(){
    hamburger.addEventListener('click', () => {
    if (sideMenu.classList.contains('hidden')) {
        sideMenu.classList.remove('hidden');
    }else{
        sideMenu.classList.add('hidden');
    }
}
)}


// ham.addEventListener('click', () => {
//     if (main_content.classList.contains('w-4/5')) {
//         menu.classList.remove('w-4/5');
//     }else{
//         menu.classList.add('w-4/5');
//     }
// })