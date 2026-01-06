import { isLoggedIn, logout } from "./auth.js";

export async function loadNavbar() {
  const res = await fetch("/components/navbar.html");
  document.body.insertAdjacentHTML("afterbegin", await res.text());

  const links = document.getElementById("auth-links");

  if (isLoggedIn()) {
    links.innerHTML = `
      <button id="logout-btn"
        class="text-red-400 hover:text-red-300">
        Logout
      </button>`;
    document.getElementById("logout-btn").onclick = logout;
  } else {
    links.innerHTML = `
      <a href="/pages/login.html" class="hover:text-gray-300">Login</a>
      <a href="/pages/signup.html" class="hover:text-gray-300 ml-2">Sign Up</a>`;
  }
}
