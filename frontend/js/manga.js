import { loadNavbar } from "./navbar.js";
import { apiFetch } from "./api.js";

await loadNavbar();
const searchInput = document.getElementById("search");
const genreSelect = document.getElementById("genre-select");
const mangaList = document.getElementById("manga-list");

async function fetchManga({ query = "", genre = "" } = {}) {
  const params = new URLSearchParams();
  if (query) params.append("q", query);
  if (genre) params.append("genre", genre);

  return apiFetch(`/manga/?${params.toString()}`);
}

async function fetchGenres() {
  return apiFetch("/manga/genres");
}

function renderManga(list) {
  if (!list.length) {
    mangaList.innerHTML = "<p>No manga found.</p>";
    return;
  }

  mangaList.innerHTML = list
    .map(m => `
      <a href="/pages/manga-detail.html?id=${m.id}"
         class="border p-4 rounded bg-white hover:bg-gray-100">
        <h3 class="font-semibold">${m.title}</h3>
        <p class="text-gray-500">${m.year ?? ""}</p>
      </a>
    `)
    .join("");
}

function renderGenres(genres) {
  genres.forEach(g => {
    const option = document.createElement("option");
    option.value = g.name;
    option.textContent = g.name;
    genreSelect.appendChild(option);
  });
}

async function loadManga() {
  try {
    const data = await fetchManga({
      query: searchInput.value,
      genre: genreSelect.value,
    });

    const list = Array.isArray(data)
      ? data
      : data.results ?? [];

    renderManga(list);
  } catch (err) {
    mangaList.innerHTML =
      `<p class="text-red-600">${err.message}</p>`;
  }
}

async function loadGenres() {
  try {
    const genres = await fetchGenres();
    renderGenres(genres);
  } catch {
    genreSelect.innerHTML =
      `<option value="">Failed to load genres</option>`;
  }
}

searchInput.addEventListener("input", loadManga);
genreSelect.addEventListener("change", loadManga);

await loadGenres();
await loadManga();
