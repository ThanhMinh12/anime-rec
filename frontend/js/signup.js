import { apiFetch } from "./api";
document.getElementById("signup-form").onsubmit = async (e) => {
  e.preventDefault();

  const username = username.value;
  const password = password.value;

  const res = await apiFetch("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });

  localStorage.setItem("token", res.access_token);
  window.location.href = "/pages/index.html";
};