const ham = document.querySelector("#ham")
const navbar = document.querySelector("#navbar")
const main = document.querySelector("#main")

ham.addEventListener("click", function (e) {
    navbar.classList.toggle("open")
    e.target.classList.toggle("ri-menu-line")
    e.target.classList.toggle("ri-close-line")
    main.classList.toggle("blur")
})
