// Form Submission Logic
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            const resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = `
                <p><strong>Age:</strong> ${data.age}</p>
                <p><strong>Generation:</strong> ${data.generation}</p>
                <p><strong>Emotion:</strong> ${data.emotion}</p>
                <p><strong>Suggested Song:</strong> ${data.suggested_song}</p>
            `;
        } else {
            alert(data.error || "An error occurred.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while processing your request.");
    }
});

// Camera Button Logic
document.getElementById("cameraButton").addEventListener("click", () => {
    alert("Camera functionality coming soon!");
});
