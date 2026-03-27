console.log("JS LOADED");
document.addEventListener("DOMContentLoaded", function () {
  function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      if (cookie.startsWith("csrftoken=")) {
        cookieValue = cookie.substring("csrftoken=".length);
        break;
      }
    }

    return cookieValue;
  }

  document.querySelectorAll(".like-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const blogId = this.getAttribute("data-id");
      const btn = this; // preserve reference to button

      fetch(`/blog/like/${blogId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({}), // ✅ send empty JSON
      })
        .then((response) => {
          if (!response.ok) throw new Error("Network response was not OK");
          return response.json(); // parse JSON
        })
        .then((data) => {
          if (data.error) {
            alert("Login required");
            return;
          }

          // Update like count using your variable name
          const count = document.getElementById(`like-count-${blogId}`);
          count.innerText = data.count;

          // Update button text using your btn variable
          if (data.liked === true) {
            btn.innerText = "❤️ Liked";
          } else {
            btn.innerText = "🤍 Like";
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
  // 🔍 SEARCH SUGGESTION CODE

  const searchInput = document.getElementById("search-bar");
  const suggestionsBox = document.getElementById("suggestions");

  let debounceTimer;

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const query = this.value;

      clearTimeout(debounceTimer);

      debounceTimer = setTimeout(() => {
        if (query.length > 0) {
          fetch(`/blog/search-suggestions/?q=${query}`)
            .then((response) => response.json())
            .then((data) => {
              suggestionsBox.innerHTML = "";

              if (data.suggestions.length > 0) {
                suggestionsBox.style.display = "block"; // ✅ show

                data.suggestions.forEach((item) => {
                  const div = document.createElement("div");
                  div.textContent = item;

                  div.addEventListener("click", () => {
                    searchInput.value = item;
                    suggestionsBox.style.display = "none"; // ✅ hide

                    searchInput.onformdata.submit();
                  });

                  suggestionsBox.appendChild(div);
                });
              } else {
                suggestionsBox.style.display = "none"; // ✅ hide if empty
              }
            });
        } else {
          suggestionsBox.style.display = "none"; // ✅ hide if input empty
        }
      }, 300); // ✅ correct position
    });
  }
});
