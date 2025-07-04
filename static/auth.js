document.addEventListener("DOMContentLoaded", function() {
  const link = document.getElementById("auth-link");

  if (link) {
    fetch("/get-auth-url")
      .then(response => response.json())
      .then(data => {
        link.href = data.auth_url;
        console.log("Link href set to:", link.href);
      })
      .catch(error => console.error("Error fetching auth URL:", error));
  }
});
