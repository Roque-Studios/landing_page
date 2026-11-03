/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: "#060608",
        charcoal: "#121216",
        graphite: "#2A2B30",
        white: "#FFFFFF",
        grey: "#CDD2D6",
        cyan: "#00E5FF",
        green: "#3CFF78",
        red: "#E61E28",
      },
      fontFamily: {
        display: ["Bangers", "cursive"],
        comic: ["'Comic Neue'", "cursive"],
        body: ["Inter", "sans-serif"],
      },
      maxWidth: {
        content: "1280px",
      },
    },
  },
  plugins: [],
};
