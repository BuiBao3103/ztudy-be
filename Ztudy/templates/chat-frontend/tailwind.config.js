/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          900: '#111827',
          800: '#1F2937',
          700: '#374151',
          600: '#4B5563',
          500: '#6B7280',
          400: '#9CA3AF',
          300: '#D1D5DB',
        },
        'dark-bg': '#1a1a1a',
        'dark-border': '#2d2d2d',
        'primary': '#3b82f6',
        'primary-dark': '#2563eb',
      },
      animation: {
        'bounce-slow': 'bounce 1.5s infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'typing-dot-1': 'typing-dot 1s infinite',
        'typing-dot-2': 'typing-dot 1s infinite 0.2s',
        'typing-dot-3': 'typing-dot 1s infinite 0.4s',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'typing-dot': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-2px)' },
        }
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('tailwind-scrollbar')({ nocompatible: true }),
  ],
} 