import { apiFetch } from "./api.js";

document.getElementById("signup-form").onsubmit = async (e) => {
  e.preventDefault();

  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");

  const username = usernameInput.value;
  const password = passwordInput.value;

  try {
    const res = await apiFetch("/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password }),
    });

    localStorage.setItem("token", res.access_token);
    window.location.href = "/pages/index.html";
  } catch (err) {
    alert("Signup failed (username may already exist)");
  }
};
