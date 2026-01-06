import { loadNavbar } from "./navbar.js";
import { apiFetch } from "./api.js";
import { setToken } from "./auth.js";

await loadNavbar();

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const res = await apiFetch("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });

    setToken(res.access_token);
    window.location.href = "/pages/index.html";
  } catch (err) {
    alert(err?.detail || "Login failed");
  }
});
