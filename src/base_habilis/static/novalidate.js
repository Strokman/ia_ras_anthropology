var forms = document.querySelectorAll('.form-control');

for (var i = 0; i < forms.length; i++) {
    forms[i].setAttribute('novalidate', true);
}