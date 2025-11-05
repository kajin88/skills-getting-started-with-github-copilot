document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    console.log("Fetching activities...");
    try {
      const response = await fetch("/activities");
      const activities = await response.json();
      console.log("Activities fetched:", activities);

      // Clear loading message
      activitiesList.innerHTML = "";
      
      // Clear existing options in select dropdown
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Create participants list HTML
        let participantsHTML = '';
        if (details.participants.length > 0) {
          const participantsList = details.participants
            .map((participant, index) => `
              <div class="participant-item">
                <span class="participant-email">${participant}</span>
                <button class="delete-participant-btn" data-activity="${name}" data-email="${participant}" title="Remove participant">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            `)
            .join('');
          participantsHTML = `
            <div class="participants-section">
              <h5>Current Participants:</h5>
              <div class="participants-list">
                ${participantsList}
              </div>
            </div>
          `;
        } else {
          participantsHTML = `
            <div class="participants-section">
              <h5>Current Participants:</h5>
              <p class="no-participants">No participants yet</p>
            </div>
          `;
        }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsHTML}
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });

    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        
        console.log("Registration successful, refreshing activities...");
        // Refresh the activities list to show updated participant count
        await fetchActivities();
        console.log("Activities refreshed after registration");
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();

  // Add event delegation for delete buttons (set up once)
  activitiesList.addEventListener('click', (event) => {
    if (event.target.closest('.delete-participant-btn')) {
      const button = event.target.closest('.delete-participant-btn');
      const activityName = button.getAttribute('data-activity');
      const email = button.getAttribute('data-email');
      unregisterParticipant(activityName, email);
    }
  });
});

// Function to unregister a participant
async function unregisterParticipant(activityName, email) {
  if (!confirm(`Are you sure you want to unregister ${email} from ${activityName}?`)) {
    return;
  }

  try {
    const response = await fetch(
      `/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(email)}`,
      {
        method: "DELETE",
      }
    );

    console.log('Response status:', response.status);
    console.log('Response ok:', response.ok);

    // Check if response is JSON
    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      throw new Error(`Expected JSON response, got ${contentType}`);
    }

    const result = await response.json();
    console.log('Response data:', result);

    if (response.ok) {
      // Show success message
      const messageDiv = document.getElementById("message");
      messageDiv.textContent = result.message;
      messageDiv.className = "success";
      messageDiv.classList.remove("hidden");

      // Hide message after 3 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 3000);

      // Refresh the activities list to reflect the change
      await fetchActivities();
      console.log("Activities refreshed after unregistration");
    } else {
      alert(result.detail || "Failed to unregister participant");
    }
  } catch (error) {
    console.error("Detailed error:", error);
    alert(`Failed to unregister participant: ${error.message}`);
  }
}
