import { loadNavbar } from "./navbar.js";
import { apiFetch } from "./api.js";

await loadNavbar();

const searchEl = document.getElementById("search");
const genreEl = document.getElementById("genre-select");
const listEl = document.getElementById("manga-list");

async function loadGenres() {
  const genres = await apiFetch("/manga/genres");
  genres.forEach(g => {
    const opt = document.createElement("option");
    opt.value = g.name;
    opt.textContent = g.name;
    genreEl.appendChild(opt);
  });
}

async function loadManga(query = "", genre = "") {
  const params = new URLSearchParams();
  if (query) params.append("q", query);
  if (genre) params.append("genre", genre);

  const data = await apiFetch(`/manga/?${params.toString()}`);
  const list = Array.isArray(data) ? data : (data.results || []);

  listEl.innerHTML = list.length
    ? list.map(m => `
        <a href="/pages/manga-detail.html?id=${m.id}"
           class="border p-4 rounded bg-white hover:bg-gray-100">
          <h3 class="font-semibold">${m.title}</h3>
          <p class="text-gray-500">${m.year ?? ""}</p>
        </a>
      `).join("")
    : "<p>No manga found.</p>";
}

searchEl.addEventListener("input", (e) => {
  loadManga(e.target.value, genreEl.value);
});

genreEl.addEventListener("change", (e) => {
  loadManga(searchEl.value, e.target.value);
});

await loadGenres();
await loadManga();
