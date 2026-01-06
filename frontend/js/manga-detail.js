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


async function loadRelatedManga() {
  try {
    const data = await apiFetch(`/recommendations/${id}`);
    const recs = data.recommendations;
    if (!recs || recs.length === 0) {
      document.getElementById("related").innerHTML =
        "<p class='text-gray-500'>No related manga found.</p>";
      return;
    }
    document.getElementById("related").innerHTML = recs.map(m => `
      <a
        href="manga-detail.html?id=${m.id}"
        class="border p-3 rounded bg-white hover:bg-gray-100"
      >
        <h3 class="font-semibold">${m.title}</h3>
        <p class="text-sm text-gray-500">${m.year ?? ""}</p>
      </a>
    `).join("");
  } catch (err) {
    document.getElementById("related").innerHTML =
      "<p class='text-gray-500'>No related manga found.</p>";
  }
}


await loadRelatedManga();

const form = document.getElementById("review-form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const rating = Number(document.getElementById("rating").value);
  const text = document.getElementById("review-text").value;

  if (!rating || rating < 1 || rating > 10) {
    alert("Rating must be between 1 and 10");
    return;
  }

  try {
    await apiFetch("/reviews", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        manga_id: Number(id),
        rating,
        text: text || null
      })
    });

    form.reset();
    await loadReviews();
  } catch (err) {
    console.error(err);
    alert("Pls log in");
  }
});
