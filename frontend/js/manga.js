import { loadNavbar } from "./navbar.js";
import { apiFetch } from "./api.js";

await loadNavbar();
let offset = 0;
const LIMIT = 20;
let loading = false;
let hasMore = true;
let currentQuery = "";
let currentGenre = "";
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

async function loadManga(query = "", genre = "", reset = false) {
  if (loading || !hasMore) return;
  loading = true;

  
  if (reset) {
    offset = 0;
    hasMore = true;
    listEl.innerHTML = "";
    currentQuery = query;
    currentGenre = genre;
  }
  const params = new URLSearchParams({
    limit: LIMIT,
    offset,
  });

  if (currentQuery) params.append("q", currentQuery);
  if (currentGenre) params.append("genre", currentGenre);



  const list = await apiFetch(`/manga/?${params.toString()}`);
  if (!list.length) {
    hasMore = false;
  } else {
    listEl.insertAdjacentHTML(
      "beforeend",

      list.map(m => `
        <a href="/pages/manga-detail.html?id=${m.id}"
           class="border p-4 rounded bg-white hover:bg-gray-100">
          <h3 class="font-semibold">${m.title}</h3>
          <p class="text-gray-500">${m.year ?? ""}</p>
        </a>
      `).join("")
    );

    offset += LIMIT;
  }
  loading = false;
}

searchEl.addEventListener("input", (e) => {
  loadManga(e.target.value, genreEl.value, true);
});

genreEl.addEventListener("change", (e) => {
  loadManga(searchEl.value, e.target.value, true);
});
const sentinel = document.createElement("div");
sentinel.className = "h-10";
listEl.after(sentinel);
const observer = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) {
    loadManga();
  }
}, { rootMargin: "300px" });
observer.observe(sentinel);
await loadGenres();
await loadManga("", "", true);
