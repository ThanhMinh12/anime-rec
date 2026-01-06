import { isLoggedIn, clearToken } from "./auth.js";

export async function loadNavbar() {
  const host = document.getElementById("navbar");
  if (!host) return;

  const res = await fetch("/components/navbar.html");
  host.innerHTML = await res.text();

  updateAuthLinks();
}

function updateAuthLinks() {
  const links = document.getElementById("auth-links");
  if (!links) return;

  if (isLoggedIn()) {
    links.innerHTML = `
      <button id="logout-btn" class="text-red-400 hover:text-red-300">Logout</button>
    `;
    document.getElementById("logout-btn").addEventListener("click", () => {
      clearToken();
      window.location.href = "/pages/index.html";
    });
  } else {
    links.innerHTML = `
      <a href="/pages/login.html" class="hover:text-gray-300">Login</a>
      <a href="/pages/signup.html" class="hover:text-gray-300 ml-2">Sign Up</a>
    `;
  }
}
