import { loadNavbar } from "./navbar.js";
import { apiFetch } from "./api.js";

await loadNavbar();

const id = new URLSearchParams(window.location.search).get("id");

const manga = await apiFetch(`/manga/${id}`);
document.getElementById("manga").innerHTML = `
  <h1 class="text-4xl font-bold">${manga.title}</h1>
  <p class="text-gray-600">${manga.year || ""}</p>
  <p class="mt-4">${manga.synopsis || ""}</p>
`;

async function loadReviews() {
  try {
    const reviews = await apiFetch(`/reviews/manga/${id}`);
    document.getElementById("reviews").innerHTML = reviews.map(r => `
      <div class="border p-3 rounded bg-white">
        <p class="font-bold">Rating: ${r.rating}/10</p>
        <p>${r.text || ""}</p>
      </div>
    `).join("");
  } catch {
    document.getElementById("reviews").innerHTML =
      "<p class='text-gray-500'>No reviews yet.</p>";
  }
}

loadReviews();
