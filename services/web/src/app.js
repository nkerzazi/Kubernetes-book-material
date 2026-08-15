import L from "leaflet";

const API = import.meta.env.VITE_API_URL || "/api";
const carte = L.map("carte").setView([43.35, 4.9], 8);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap",
}).addTo(carte);

const marqueurs = new Map();

async function rafraichir() {
  try {
    const reponse = await fetch(`${API}/navires`);
    const { navires } = await reponse.json();
    document.getElementById("etat").textContent =
      `${navires.length} navires suivis — ${new Date().toLocaleTimeString("fr-FR")}`;

    const lignes = [];
    for (const navire of navires) {
      if (navire.position) {
        const { latitude, longitude } = navire.position;
        if (marqueurs.has(navire.imo)) {
          marqueurs.get(navire.imo).setLatLng([latitude, longitude]);
        } else {
          marqueurs.set(
            navire.imo,
            L.circleMarker([latitude, longitude], { radius: 6, color: "#2e9e5b" })
              .bindTooltip(navire.nom)
              .addTo(carte)
          );
        }
      }
      lignes.push(
        `<tr><td>${navire.nom}</td><td>${navire.destination}</td>` +
        `<td class="eta">${navire.eta_minutes ?? "—"}</td></tr>`
      );
    }
    document.getElementById("liste").innerHTML = lignes.join("");
  } catch (erreur) {
    document.getElementById("etat").textContent = "API injoignable";
  }
}

rafraichir();
setInterval(rafraichir, 2000);
