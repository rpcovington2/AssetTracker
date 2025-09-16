const form = document.getElementById('expense-form');

form.addEventListener('submit', (event) => {
    event.preventDefault();
    var name = document.getElementById('expense-name').value;
    var comment = document.getElementById('expense-comment').value;

    console.log(name);
    console.log(comment);
});

console.log(form)