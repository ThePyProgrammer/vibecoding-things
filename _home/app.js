const experiments = [
  {
    title: "Atari Combat",
    subtitle: "Two tanks enter. Browser tab leaves.",
    description:
      "A crunchy two-player tank game with pixel-era swagger, glowing scoreboards, and absolutely no HR department.",
    href: "combat/",
    screenshot: "_home/screenshots/combat.png",
    category: "game",
    tool: "Claude Web App",
    model: "Claude Sonnet 3.6",
    prompts: 1,
    status: "Playable",
    tags: ["Arcade", "Canvas", "Two-player"]
  },
  {
    title: "Combat 3D",
    subtitle: "The same bad decisions, now with depth perception.",
    description:
      "A first-person-ish 3D tank arena that answers the question: what if Atari had a suspicious WebGL budget?",
    href: "combat/3d.html",
    screenshot: "_home/screenshots/combat-3d.png",
    category: "game",
    tool: "Claude Web App",
    model: "Claude Sonnet 3.6",
    prompts: 3,
    status: "Playable",
    layout: "wide",
    tags: ["3D", "WebGL", "Tanks"]
  },
  {
    title: "Jedi Duel",
    subtitle: "A lightsaber fight with strong school-project confidence.",
    description:
      "A cinematic duel where the health bars glow, the sabers glow, and the legal department is not invited.",
    href: "lightsabers/",
    screenshot: "_home/screenshots/lightsabers.png",
    category: "game",
    tool: "Claude Web App",
    model: "Claude Sonnet 3.6",
    prompts: 1,
    status: "Playable",
    tags: ["3D", "Duel", "Lightsabers"]
  },
  {
    title: "Angry Birds 3D",
    subtitle: "Physics, architecture, and unresolved bird feelings.",
    description:
      "A projectile playground with piggy targets and enough 3D ambition to make the browser ask for a minute.",
    href: "angrybirds/",
    screenshot: "_home/screenshots/angrybirds.png",
    category: "game",
    tool: "Claude Web App",
    model: "Claude Sonnet 3.6",
    prompts: 2,
    status: "Playable",
    tags: ["3D", "Physics", "Bird logistics"]
  },
  {
    title: "MIPS Simulator",
    subtitle: "For when assembly needs a dramatic lighting rig.",
    description:
      "A visual MIPS architecture simulator that makes registers, instructions, and datapaths feel like a tiny sci-fi control room.",
    href: "mips/",
    screenshot: "_home/screenshots/mips.png",
    category: "tool",
    tool: "Claude Web App",
    model: "Claude Sonnet 3.6",
    prompts: 1,
    status: "Usable",
    tags: ["Simulator", "Architecture", "Learning"]
  },
  {
    title: "Closest MRT Finder",
    subtitle: "Singapore transit, but make it oddly personal.",
    description:
      "A practical little station finder wrapped in map-table energy, built because sometimes the useful idea also deserves a weird shelf.",
    href: "closest_mrt/",
    screenshot: "_home/screenshots/closest-mrt.png",
    category: "tool",
    tool: "Codex TUI",
    model: "GPT 5.5",
    prompts: 5,
    status: "Useful",
    layout: "showcase",
    tags: ["Transit", "Singapore", "Python"]
  },
  {
    title: "Breadboards",
    subtitle: "A circuit sandbox currently wearing a lab coat.",
    description:
      "A 3D breadboard experiment for poking at circuits in the browser. Categorized as a prototype because it knows what it did.",
    href: "breadboards/",
    screenshot: "_home/screenshots/breadboards.png",
    category: "prototype",
    tool: "Codex / Vite",
    model: "Mixed",
    prompts: 0,
    status: "Prototype",
    tags: ["Circuits", "React", "3D"]
  }
];

const gallery = document.querySelector("#shelf");
const filters = document.querySelectorAll(".filter");

function renderShelf(filter = "all") {
  const visible = experiments.filter((experiment) => filter === "all" || experiment.category === filter);

  gallery.innerHTML = visible
    .map(
      (experiment, index) => `
        <a
          class="gallery-card ${experiment.layout || ""} ${index % 5 === 0 ? "featured" : ""} ${index % 4 === 2 ? "tall" : ""}"
          style="--delay: ${index * 45}ms; --ratio: ${index % 4 === 2 ? "3 / 4" : "1 / 1"}"
          href="${experiment.href}"
          aria-label="Open ${experiment.title}: ${experiment.tags.join(", ")}"
        >
          <img src="${experiment.screenshot}" alt="Screenshot of ${experiment.title} in action" loading="lazy">
          <div class="overlay" aria-hidden="true">
            <div>
              <h2>${experiment.title}</h2>
              <p>${experiment.subtitle}</p>
            </div>
            <div class="tag-row">
              ${[experiment.category, ...experiment.tags].map((tag) => `<span>${tag}</span>`).join("")}
            </div>
          </div>
        </a>
      `
    )
    .join("");
}

filters.forEach((button) => {
  button.addEventListener("click", () => {
    filters.forEach((filter) => filter.classList.remove("active"));
    button.classList.add("active");
    renderShelf(button.dataset.filter);
  });
});

renderShelf();
