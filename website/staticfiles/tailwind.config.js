/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../../**/templates/**/*.html',
    '../../**/static/**/*.js',
    '../../**/static/**/*.css',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("daisyui")
  ],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
}
