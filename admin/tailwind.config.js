/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#0F6E56",
        secondary: "#BA7517",
        danger: "#E24B4A",
      }
    },
  },
  plugins: [],
}
