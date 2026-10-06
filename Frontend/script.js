
const API_URL = "";

async function diagnoseProblem() {
    const problem = document.getElementById("problem").value.trim();
    const image = document.getElementById("image").files[0];
    const button = document.getElementById("diagnoseButton");

    if (!problem && !image) {
        alert("Please describe your problem or upload a screenshot.");
        return;
    }

    button.disabled = true;
    button.textContent = "Analyzing...";

    try {
        let data;

        if (image) {
            const formData = new FormData();
            formData.append("file", image);

            const response = await fetch(
                `${API_URL}/analyze-image`,
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {
                throw new Error("Image analysis failed.");
            }

            const result = await response.json();

            if (!result.diagnosis) {
                throw new Error("No diagnosis returned from image analysis.");
            }

            data = result.diagnosis;

        } else {

            const response = await fetch(
                `${API_URL}/diagnose`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        problem: problem
                    })
                }
            );

            if (!response.ok) {
                throw new Error("Diagnosis failed.");
            }

            const result = await response.json();

            if (!result.result) {
                throw new Error("No diagnosis returned.");
            }

            data = result.result;
        }

        document.getElementById("diagnosis").textContent =
            data.diagnosis;

        document.getElementById("category").textContent =
            data.category;

        document.getElementById("confidence").textContent =
            data.confidence;

        const solutionList =
            document.getElementById("solutionList");

        solutionList.innerHTML = "";

        data.solution.forEach((step) => {

            const li = document.createElement("li");

            li.textContent = step;

            solutionList.appendChild(li);
        });

        const supportBox =
            document.getElementById("supportBox");

        if (data.it_required) {

            supportBox.classList.remove("hidden");

        } else {

            supportBox.classList.add("hidden");
        }

        const resultSection =
            document.getElementById("result");

        resultSection.classList.remove("hidden");

        resultSection.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        console.error("ITERA Error:", error);

        alert(
            "Something went wrong. Please make sure the ITERA server is running."
        );

    } finally {

        button.disabled = false;

        button.textContent = "Analyze Problem";
    }
}


function contactIT() {

    alert(
        "Please contact your company's IT Support team."
    );
}
