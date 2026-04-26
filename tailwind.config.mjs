/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx,vue,svelte}"],
  theme: {
    extend: {
      colors: {
        // Claude Code inspired palette: warm off-white surface,
        // deep warm neutrals for type, terracotta accent.
        paper: {
          50: "#FAF7F0",
          100: "#F5F1E8",
          200: "#EDE6D6",
          300: "#E0D6BE",
          400: "#C8BB9E",
        },
        ink: {
          50: "#7B756B",
          100: "#5C5650",
          200: "#403C37",
          300: "#2D2A26",
          400: "#1F1D1A",
        },
        accent: {
          50: "#FCEFE8",
          100: "#F5D6C3",
          200: "#E5A98A",
          300: "#D38A66",
          400: "#CC785C", // primary accent (Claude terracotta)
          500: "#B26649",
          600: "#8F4F38",
        },
        moss: {
          400: "#7A8B5C", // secondary accent for tags
          500: "#5F6F44",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
        mono: [
          "JetBrains Mono",
          "Fira Code",
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          "monospace",
        ],
        serif: [
          "Source Serif 4",
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
