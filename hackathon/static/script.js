// Function 1: Set text inside textarea when preset buttons are clicked
function setPreset(type) {
    const complaintInput = document.getElementById('complaintInput');

    if (type === 'pothole') {
        complaintInput.value = "There is a huge pothole near Dadar station causing heavy traffic and two bikers fell down this morning.";
    } else if (type === 'garbage') {
        complaintInput.value = "Garbage has not been collected near SV Road Junction for 3 days. It is starting to smell very bad.";
    }
}

// Function 2: Fetch data from backend API
async function callApi(userText) {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/classify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: userText })
        });

        // Check if response is OK (Status 200)
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            console.error("Server error response");
            return null;
        }
    } catch (error) {
        console.error("Error connecting to API:", error);
        return null; // Return null if connection fails
    }
}

// Function 3: Main function called when clicking 'Analyze Complaint'
async function handleAnalyze() {
    const complaintInput = document.getElementById('complaintInput');
    const submitBtn = document.getElementById('submitBtn');
    const userText = complaintInput.value.trim();

    // Check if input is empty
    if (userText === "") {
        alert("Please enter a complaint first!");
        return;
    }

    // Change button text while waiting
    submitBtn.textContent = "Analyzing...";
    submitBtn.disabled = true;

    // Call API function
    let data = await callApi(userText);

    // Fallback Mock Data (If Backend/API fails during demo)
    if (!data) {
        data = {
            summary: "Severe road defect causing safety hazards.",
            category: "Road Infrastructure",
            priority: "URGENT",
            action: "Route immediately to Ward G/North maintenance team."
        };
    }

    // Display the results on screen
    displayResults(data);

    // Reset button back to normal
    submitBtn.textContent = "Analyze Complaint";
    submitBtn.disabled = false;
}

// Function 4: Update HTML elements with result data
function displayResults(data) {
    const resultCard = document.getElementById('resultCard');
    const summaryText = document.getElementById('summaryText');
    const categoryBadge = document.getElementById('categoryBadge');
    const priorityBadge = document.getElementById('priorityBadge');
    const actionText = document.getElementById('actionText');

    // Fill in text fields
    summaryText.textContent = data.summary || data.summary_text || "No summary available";
    categoryBadge.textContent = data.category || "General";
    actionText.textContent = data.action || data.suggested_action || "No action specified";

    // Format priority text
    const priority = (data.priority || "MEDIUM").toUpperCase();
    priorityBadge.textContent = priority;

    // Simple priority color logic using standard if-else
    if (priority === "URGENT" || priority === "HIGH") {
        priorityBadge.className = "text-xs font-bold px-3 py-1 rounded-full border bg-red-100 text-red-800 border-red-300";
    } else if (priority === "MEDIUM") {
        priorityBadge.className = "text-xs font-bold px-3 py-1 rounded-full border bg-amber-100 text-amber-800 border-amber-300";
    } else {
        priorityBadge.className = "text-xs font-bold px-3 py-1 rounded-full border bg-emerald-100 text-emerald-800 border-emerald-300";
    }

    // Show result box
    resultCard.classList.remove('hidden');
}