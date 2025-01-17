document.addEventListener("DOMContentLoaded", () => {
    const instructionBox = document.getElementById("instructionText");
    const startButton = document.getElementById("startButton");
    const nextButton = document.getElementById("nextButton");
    const previousButton = document.getElementById("previousButton");
    const repeatButton = document.getElementById("repeatButton");
    const explainButton = document.getElementById("explainButton");

    let currentStep = 0;
    const steps = [
        "Step 1: Fill a pot with water and place it on the stove.",
        "Step 2: Turn on the stove and wait for the water to boil.",
        "Step 3: Add pasta to the boiling water.",
        "Step 4: Stir occasionally to prevent sticking.",
        "Step 5: Drain the pasta after 10 minutes."
    ];

    function updateInstruction(step) {
        if (step < steps.length && step >= 0) {
            instructionBox.innerText = steps[step];
            nextButton.disabled = step === steps.length - 1;
            previousButton.disabled = step === 0;
        } else {
            instructionBox.innerText = "You have completed the cooking task!";
            nextButton.disabled = true;
            previousButton.disabled = true;
        }
    }

    startButton.addEventListener("click", () => {
        currentStep = 0;
        updateInstruction(currentStep);
        nextButton.disabled = false;
        previousButton.disabled = true;
        repeatButton.disabled = false;
        explainButton.disabled = false;
        startButton.disabled = true;
    });

    nextButton.addEventListener("click", () => {
        if (currentStep < steps.length - 1) {
            currentStep++;
            updateInstruction(currentStep);
        }
    });

    previousButton.addEventListener("click", () => {
        if (currentStep > 0) {
            currentStep--;
            updateInstruction(currentStep);
        }
    });

    repeatButton.addEventListener("click", () => {
        instructionBox.innerText = steps[currentStep];
    });

    explainButton.addEventListener("click", () => {
        alert(`Explanation: This step is important because it prepares the base for your pasta.`);
    });
});