import { apiFetch } from "./api.js";

document.getElementById("login-form").onsubmit = async (e) => {
  e.preventDefault();

  const username = username.value;
  const password = password.value;

  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });

  localStorage.setItem("token", res.access_token);
  window.location.href = "/pages/index.html";
};
