let currentStep = 0;
    let steps = [];

    document.addEventListener("DOMContentLoaded", () => {
        const instructionBox = document.getElementById("instructionText");
        const startButton = document.getElementById("startButton");
        const nextButton = document.getElementById("nextButton");
        const previousButton = document.getElementById("previousButton");
        const repeatButton = document.getElementById("repeatButton");
        const explainButton = document.getElementById("explainButton");

        fetch('/Pasta_Cooking/steps_config_updated.json')
            .then(response => response.json())
            .then(data => {
                steps = data.steps;
            })
            .catch(error => console.error('Error loading steps:', error));

        function updateInstruction(stepIndex) {
            const step = steps[stepIndex];
            if (step) {
                instructionBox.innerText = step.instruction;
                nextButton.disabled = stepIndex === steps.length - 1;
                previousButton.disabled = stepIndex === 0;
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
            instructionBox.innerText = steps[currentStep].instruction;
        });

        explainButton.addEventListener("click", () => {
            const explanation = steps[currentStep].explanation || "No explanation available.";
            alert(`Explanation: ${explanation}\nSafety Reminder: ${steps[currentStep].safety_reminder || "No safety reminder available."}`);
        });

        window.addEventListener("updateInstruction", (event) => {
            const detail = event.detail;
            instructionBox.innerText = detail.instruction || "No instruction provided.";
        });
    });