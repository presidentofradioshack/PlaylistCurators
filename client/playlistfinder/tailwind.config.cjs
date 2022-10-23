/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		"./index.html",
		"./src/**/*.{js,ts,jsx,tsx}",
	],
	theme: {
		extend: {
			colors: {
				gray: {
					900: '#121212',
					800: '#212121',
					700: '#535353',
					600: '#B3B3B3'
				},
				'spotify-green': '#1DB954'
			},
			fontFamily: {
				'almanach': ['almanach', 'sans-serif'],
			}
		},
	},
	plugins: [
		require('@tailwindcss/forms')
	],
}