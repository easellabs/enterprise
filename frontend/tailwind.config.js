module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",  // Ensure Tailwind scans your files for utility classes
  ],
  theme: {
    extend: {
      colors: {
        brandBlue: '#1DA1F2',
        brandGray: '#8899A6',
      },
      animation: {
        fadeIn: 'fadeIn 2s ease-in forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
};
