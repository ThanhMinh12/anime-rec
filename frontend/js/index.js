import { loadNavbar } from "./navbar.js";
import { apiFetch } from "./api.js";

await loadNavbar();

const random = await apiFetch("/manga/random");
document.getElementById("random").innerHTML = `
  <h2 class="text-xl font-semibold">${random.title}</h2>
  <p class="text-gray-600">${random.year || ""}</p>
`;

const trending = await apiFetch("/manga/trending");
document.getElementById("trending").innerHTML = trending
  .map(t => `
    <a href="/pages/manga-detail.html?id=${t.manga.id}"
      class="border p-4 rounded bg-white hover:bg-gray-100">
      <h3 class="font-semibold">${t.manga.title}</h3>
      <p class="text-gray-500">${t.reviews} reviews</p>
    </a>
  `)
  .join("");
