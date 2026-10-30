// Índice lateral, citas [n] enlazadas a su fuente y clases para las listas de acciones y fuentes.
(() => {
  const doc = document.querySelector(".doc");
  if (!doc) return;
  const h2s = [...doc.querySelectorAll("h2")];
  const tras = (h) => { let el = h.nextElementSibling; while (el && el.tagName !== "OL" && el.tagName !== "H2") el = el.nextElementSibling; return el && el.tagName === "OL" ? el : null; };
  const hFuentes = h2s.find((h) => /^fuentes/i.test(h.textContent.trim()));
  const hPasos = h2s.find((h) => /^qué puedes hacer/i.test(h.textContent.trim()));
  const fuentes = hFuentes && tras(hFuentes);
  if (hPasos && tras(hPasos)) tras(hPasos).classList.add("pasos");
  const titulos = {};
  if (fuentes) {
    fuentes.classList.add("fuentes");
    [...fuentes.children].forEach((li, i) => {
      li.id = `fuente-${i + 1}`;
      titulos[i + 1] = li.textContent.replace(/https?:\/\/\S+/g, "").trim().replace(/\.$/, "");
    });
  }
  // [12] o [1][5] en el texto pasan a chips que saltan a la fuente
  const walker = document.createTreeWalker(doc, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (fuentes && fuentes.contains(n)) || n.parentElement.closest("code, a") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
  const nodos = [];
  while (walker.nextNode()) if (/\[\d+\]/.test(walker.currentNode.nodeValue)) nodos.push(walker.currentNode);
  for (const n of nodos) {
    const frag = document.createDocumentFragment();
    n.nodeValue.split(/(\[\d+\])/).forEach((parte) => {
      const m = parte.match(/^\[(\d+)\]$/);
      if (!m || !titulos[m[1]]) return parte && frag.append(parte);
      const a = Object.assign(document.createElement("a"), { className: "cita", href: `#fuente-${m[1]}`, textContent: m[1], title: titulos[m[1]] });
      frag.append(a);
    });
    n.replaceWith(frag);
  }
  // Índice con la misma numeración que las secciones
  const indice = document.getElementById("indice");
  const enlaces = h2s.map((h, i) => {
    const a = document.createElement("a");
    a.href = `#${h.id}`;
    a.innerHTML = `<span>${String(i + 1).padStart(2, "0")}</span>`;
    a.append(h.textContent);
    const li = document.createElement("li"); li.append(a); indice.append(li);
    return a;
  });
  const obs = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => { if (e.isIntersecting) enlaces.forEach((a, i) => a.classList.toggle("activo", h2s[i] === e.target)); });
  }, { rootMargin: "-20% 0px -70% 0px" });
  h2s.forEach((h) => obs.observe(h));
})();
