function ShowPassword(){
    var contra = document.getElementById('contra')
    var show = document.getElementById('show')
    
    if (contra.type === "password") {
        contra.type = "text";
        show.setAttribute('src', '/static/img/eye-hidden.svg')
    } else {
        contra.type = "password";
        show.setAttribute('src', '/static/img/eye-show.svg')
    }
}