const plugin = require('tailwindcss/plugin');
const flattenColorPalette = require('tailwindcss/lib/util/flattenColorPalette').default;

// https://github.com/tailwindlabs/tailwindcss/discussions/8411
module.exports = plugin(({theme, matchUtilities}) => {
    matchUtilities(
        {
            'underline-animate-color': (color) => ({
                '&::after': {
                    borderColor: color,
                }
            })
        },
        {
            values: flattenColorPalette(theme('borderColor')),
            type: 'color',
        }
    ),
    matchUtilities(
        {
            'underline-animate-duration': (duration) => ({
                '&::after': {
                    transitionDuration: duration,
                }
            })
        },
        {
            values: theme('transitionDuration'),
            type: ['number', 'any'],
        }
    )
})