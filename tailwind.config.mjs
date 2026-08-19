/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx,vue,svelte}"],
  theme: {
    extend: {
      colors: {
        // Quiet research-notebook palette: warm neutral paper, graphite type,
        // and one technical blue reserved for state and navigation.
        paper: {
          50: "#F7F7F4",
          100: "#F0F0EB",
          200: "#DEDED6",
          300: "#C7C7BC",
          400: "#A9A99D",
        },
        ink: {
          50: "#77776E",
          100: "#55554E",
          200: "#343430",
          300: "#20201D",
          400: "#11110F",
        },
        accent: {
          50: "#EEF2FF",
          100: "#DCE5FF",
          200: "#B9CAFF",
          300: "#86A4FF",
          400: "#315EFB",
          500: "#2448D8",
          600: "#1835A8",
        },
        moss: {
          400: "#537A66",
          500: "#3E6250",
        },
      },
      fontFamily: {
        sans: [
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
        mono: [
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          "monospace",
        ],
        serif: [
          "Iowan Old Style",
          "Palatino Linotype",
          "Book Antiqua",
          "ui-serif",
          "Georgia",
          "Cambria",
          "Times New Roman",
          "serif",
        ],
      },
      maxWidth: {
        prose: "72ch",
      },
      boxShadow: {
        soft: "0 1px 2px 0 rgba(45, 42, 38, 0.04), 0 4px 16px -4px rgba(45, 42, 38, 0.06)",
      },
    },
  },
  plugins: [],
};
