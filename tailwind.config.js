/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-red': '#FF4444',
        'primary-blue': '#4A90E2',
        'warning-yellow': '#F5A623',
        'success-green': '#7ED321',
        'background': '#F8F9FA',
        'card-bg': '#FFFFFF',
        'text-primary': '#2C3E50',
        'text-secondary': '#7F8C8D',
        'border': '#E9ECEF'
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif']
      },
      boxShadow: {
        'card': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'card-hover': '0 4px 16px rgba(0, 0, 0, 0.15)'
      }
    },
  },
  plugins: [],
}
