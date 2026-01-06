import { loadNavbar } from "./navbar.js";
import { apiFetch } from "./api.js";

await loadNavbar();

const randomEl = document.getElementById("random");
const trendingEl = document.getElementById("trending");

const manga = await apiFetch("/manga/random");
randomEl.innerHTML = `
  <h2 class="text-xl font-semibold">${manga.title}</h2>
  <p class="text-gray-600">${manga.year || ""}</p>
  <a class="text-blue-600" href="/pages/manga-detail.html?id=${manga.id}">
    View Details →
  </a>
`;

const data = await apiFetch("/manga/trending");
trendingEl.innerHTML = data.map(item => `
  <a href="/pages/manga-detail.html?id=${item.manga.id}"
     class="border p-4 rounded bg-white hover:bg-gray-100">
    <h3 class="font-semibold">${item.manga.title}</h3>
    <p class="text-gray-500">${item.reviews} reviews</p>
  </a>
`).join("");
