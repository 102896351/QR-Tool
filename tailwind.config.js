/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'Inter',
          '"PingFang SC"',
          '"Hiragino Sans GB"',
          '"Microsoft YaHei"',
          'system-ui',
          'sans-serif'
        ]
      },
      colors: {
        brand: {
          50:  '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81'
        }
      },
      boxShadow: {
        glass: '0 10px 40px -10px rgba(79, 70, 229, 0.18), 0 4px 12px -4px rgba(168, 85, 247, 0.12)',
        'glass-dark': '0 10px 40px -10px rgba(0, 0, 0, 0.5), 0 4px 12px -4px rgba(99, 102, 241, 0.18)',
        'glow-brand': '0 0 0 4px rgba(99, 102, 241, 0.18)'
      },
      backgroundImage: {
        'mesh-light': 'radial-gradient(at 12% 18%, rgba(165, 180, 252, 0.45) 0px, transparent 50%), radial-gradient(at 88% 12%, rgba(196, 181, 253, 0.45) 0px, transparent 50%), radial-gradient(at 30% 88%, rgba(186, 230, 253, 0.45) 0px, transparent 50%), radial-gradient(at 80% 80%, rgba(251, 207, 232, 0.4) 0px, transparent 50%)',
        'mesh-dark': 'radial-gradient(at 12% 18%, rgba(99, 102, 241, 0.25) 0px, transparent 50%), radial-gradient(at 88% 12%, rgba(168, 85, 247, 0.25) 0px, transparent 50%), radial-gradient(at 30% 88%, rgba(14, 165, 233, 0.18) 0px, transparent 50%), radial-gradient(at 80% 80%, rgba(236, 72, 153, 0.18) 0px, transparent 50%)'
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out both',
        'slide-up': 'slideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) both',
        'shimmer': 'shimmer 2.5s linear infinite',
        'float': 'float 6s ease-in-out infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 }
        },
        slideUp: {
          '0%': { opacity: 0, transform: 'translateY(16px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' }
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' }
        }
      }
    }
  },
  plugins: []
}
