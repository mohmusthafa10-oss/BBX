const steps = document.querySelectorAll(".step");
const nextButtons = document.querySelectorAll(".next");
const backButtons = document.querySelectorAll(".back");

let currentStep = 0;

// Show only the current step
function showStep() {
    steps.forEach((step, index) => {
        step.style.display = index === currentStep ? "block" : "none";
    });
}

// Next button
nextButtons.forEach(button => {
    button.addEventListener("click", () => {
        if (currentStep < steps.length - 1) {
            currentStep++;
            showStep();
        }
    });
});

// Back button
backButtons.forEach(button => {
    button.addEventListener("click", () => {
        if (currentStep > 0) {
            currentStep--;
            showStep();
        }
    });
});

// Start with Step 1
showStep();