/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',  // Paths to all HTML and JS files where Tailwind classes are used
    './templates/**/*.html',               // Add this if you're using an HTML structure in a "templates" directory
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
