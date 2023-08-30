package main

import (
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/theme"
)

type iqTheme struct {
}

func (t *iqTheme) Color(n fyne.ThemeColorName, v fyne.ThemeVariant) color.Color {
	switch n {
	case theme.ColorNameBackground, theme.ColorNameInputBackground: /*theme.ColorNamePopupBackground:*/
		return color.NRGBA{R: 39, G: 49, B: 66, A: 255} // Azul oscuro
	case theme.ColorNameForeground:
		return color.NRGBA{R: 255, G: 255, B: 255, A: 255} // Blanco
	case theme.ColorNamePrimary:
		return color.NRGBA{R: 88, G: 166, B: 157, A: 255} // Verde azulado
	case theme.ColorNameButton, theme.ColorNameFocus /*, theme.ColorNameHighlight*/, theme.ColorNameSelection:
		return color.NRGBA{R: 120, G: 187, B: 176, A: 200} // Verde claro con transparencia
	}

	return theme.DefaultTheme().Color(n, v)
}

func (t *iqTheme) Font(s fyne.TextStyle) fyne.Resource {
	// Aquí puedes cargar y retornar una fuente personalizada si lo deseas
	return theme.DefaultTheme().Font(s)
}

func (t *iqTheme) Icon(n fyne.ThemeIconName) fyne.Resource {
	// Aquí puedes cargar y retornar iconos personalizados si lo deseas
	return theme.DefaultTheme().Icon(n)
}

func (t *iqTheme) Size(n fyne.ThemeSizeName) float32 {
	// Puedes personalizar tamaños aquí, si es necesario
	return theme.DefaultTheme().Size(n)
}

// Crea una nueva instancia de nuestro tema personalizado
func NewIQTheme() fyne.Theme {
	return &iqTheme{}
}
