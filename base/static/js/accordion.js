const accordionToggle = document.querySelectorAll('.accordion-header');
const accordionBodies = document.querySelectorAll('.accordion-body');



accordionToggle.forEach(button => {
   
    button.addEventListener("click", (e) => {
        e.preventDefault();
         accordionBodies.forEach(body => {
        if (body.classList.contains('open') && !(body == e.target.nextElementSibling)) {
            body.classList.remove('open')
        }
        console.log(e.target.nextElementSibling)
        if(body == e.target.nextElementSibling) {
            body.classList.toggle('open')
        }
    })
    })
})

