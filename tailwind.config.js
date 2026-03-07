/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./home/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        samsung: {
          blue: '#1428A0',
          light: '#4A90E2',
          dark: '#0b1d5c',
          royal: '#0047AB',
          sky: '#1E90FF',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Poppins', 'Helvetica Neue', 'Arial', 'sans-serif'],
        poppins: ['Poppins', 'sans-serif'],
        inter: ['Inter', 'sans-serif'],
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.8s ease-out forwards',
        'fade-in-up-delay-1': 'fadeInUp 0.8s ease-out 0.15s forwards',
        'fade-in-up-delay-2': 'fadeInUp 0.8s ease-out 0.3s forwards',
        'fade-in-up-delay-3': 'fadeInUp 0.8s ease-out 0.45s forwards',
        'float': 'float 6s ease-in-out infinite',
        'slide-in-right': 'slideInRight 0.6s ease-out forwards',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-12px)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(30px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },
    },
  },
  plugins: [],
}
