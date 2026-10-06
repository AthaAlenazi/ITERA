const API_URL = "http://127.0.0.1:8000";


async function diagnoseProblem() {

    const problem =
        document.getElementById("problem").value.trim();

    const image =
        document.getElementById("image").files[0];

    const button =
        document.getElementById("diagnoseButton");


    // =========================
    // VALIDATION
    // =========================

    if (!problem && !image) {

        alert(
            "Please describe your problem or upload a screenshot."
        );

        return;
    }


    // =========================
    // LOADING
    // =========================

    button.disabled = true;
    button.textContent = "Analyzing...";


    try {

        let data;


        // =========================
        // IMAGE DIAGNOSIS
        // =========================

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

                throw new Error(
                    "Image analysis failed."
                );

            }


            const result =
                await response.json();


            if (!result.diagnosis) {

                throw new Error(
                    "No diagnosis returned from image analysis."
                );

            }


            data = result.diagnosis;

        }


        // =========================
        // TEXT DIAGNOSIS
        // =========================

        else {

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

                throw new Error(
                    "Diagnosis failed."
                );

            }


            const result =
                await response.json();


            if (!result.result) {

                throw new Error(
                    "No diagnosis returned."
                );

            }


            data = result.result;

        }


        // =========================
        // DISPLAY DIAGNOSIS
        // =========================

        document.getElementById(
            "diagnosis"
        ).textContent = data.diagnosis;


        // =========================
        // DISPLAY CATEGORY
        // =========================

        document.getElementById(
            "category"
        ).textContent = data.category;


        // =========================
        // DISPLAY CONFIDENCE
        // =========================

        document.getElementById(
            "confidence"
        ).textContent = data.confidence;


        // =========================
        // DISPLAY SOLUTION
        // =========================

        const solutionList =
            document.getElementById(
                "solutionList"
            );


        solutionList.innerHTML = "";


        data.solution.forEach(
            (step) => {

                const li =
                    document.createElement("li");

                li.textContent = step;

                solutionList.appendChild(li);

            }
        );


        // =========================
        // IT SUPPORT
        // =========================

        const supportBox =
            document.getElementById(
                "supportBox"
            );


        if (data.it_required) {

            supportBox.classList.remove(
                "hidden"
            );

        } else {

            supportBox.classList.add(
                "hidden"
            );

        }


        // =========================
        // SHOW RESULT
        // =========================

        const resultSection =
            document.getElementById(
                "result"
            );


        resultSection.classList.remove(
            "hidden"
        );


        resultSection.scrollIntoView({
            behavior: "smooth"
        });

    }


    // =========================
    // ERROR HANDLING
    // =========================

    catch (error) {

        console.error(
            "ITERA Error:",
            error
        );


        alert(
            "Something went wrong. Please make sure the ITERA server is running."
        );

    }


    // =========================
    // RESET BUTTON
    // =========================

    finally {

        button.disabled = false;

        button.textContent =
            "Analyze Problem";

    }

}


// =========================
// CONTACT IT
// =========================

function contactIT() {

    alert(
        "Please contact your company's IT Support team."
    );

}