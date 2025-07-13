document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function (e) {
        const age = document.querySelector('input[name="age"]').value;
        const score = document.querySelector('input[name="credit_score"]').value;

        if (age <= 0) {
            e.preventDefault();
            alert("Age must be a positive number.");
        }

        if (score < 300 || score > 850) {
            e.preventDefault();
            alert("Credit score must be between 300 and 850.");
        }
    });
});
