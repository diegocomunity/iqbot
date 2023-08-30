// dashboardAdapter.go
package adapters

import (
	"fmt"
	"image/color"
	"math/rand"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

type DashboardAdapter struct{}

func NewDashboardAdapter() *DashboardAdapter {
	return &DashboardAdapter{}
}

func (a *DashboardAdapter) ShowDashboard() {
	// Obtén la instancia actual de la aplicación
	myApp := fyne.CurrentApp()
	// Cambia el tema si es necesario (opcional)
	myApp.Settings().SetTheme(theme.LightTheme())

	topWindow := myApp.NewWindow("Dashboard")
	// Crea y muestra la ventana del dashboard en el goroutine principal
	//myWindow := myApp.NewWindow("Dashboard")
	sidebar := createSidebar()
	mainContent := createMainContent()
	// Aquí puedes construir la interfaz gráfica de la ventana de dashboard
	topWindow.SetContent(container.NewBorder(sidebar, nil, nil, nil, mainContent))
	topWindow.Resize(fyne.NewSize(640, 480))
	//myWindow.Show()
	topWindow.Show()
}

func createSidebar() fyne.CanvasObject {
	var logo = canvas.NewText("LOGO", color.NRGBA{R: 255, G: 255, B: 0, A: 255})
	logo.TextSize = 15.0
	logo.TextStyle.Bold = true
	accountMount := canvas.NewText("1200", color.Black)
	accountMount.Alignment = fyne.TextAlignCenter
	var header = container.NewHBox(logo, accountMount)
	sidebar := container.NewVBox(
		header,
		canvas.NewLine(color.White),
		/*
			widget.NewButton("Resumen del estado del robot", func() {
				showResumen()
			}),
			widget.NewButton("Lista de operaciones", func() {
				showListaOperaciones()
			}),*/

	)
	return sidebar
}

func createMainContent() fyne.CanvasObject {
	resumenTabContent := container.NewVBox(
		//widget.NewLabel("Resumen del estado del robot"),
		createPNLText(),
		// Aquí puedes agregar más widgets para mostrar el resumen
	)

	listaOperacionesTabContent := container.NewVBox(
		widget.NewLabel("Lista de operaciones"),
		// Aquí puedes agregar más widgets para mostrar la lista de operaciones
	)

	tabs := container.NewAppTabs(
		container.NewTabItem("Resumen", resumenTabContent),
		container.NewTabItem("Lista de operaciones", listaOperacionesTabContent),
	)
	tabs.SetTabLocation(container.TabLocationLeading) // Colocar las tabs en la parte superior

	return tabs
}

func createPNLText() fyne.CanvasObject /*fyne.CanvasObject */ /**widget.Label*/ {
	rand.Seed(time.Now().UnixNano())
	pnl := rand.Float32()*200.0 - 100.0 // Generar un número aleatorio entre -100 y 100
	//pnlText := fmt.Sprintf("PNL\n%.2f%%", pnl)
	pnlTittleText := fmt.Sprintf("PNL %.2f%%", pnl)
	var textColor color.Color
	if pnl >= 0 {
		textColor = color.NRGBA{R: 255, G: 255, B: 0, A: 255} // Amarillo
	} else {
		textColor = color.NRGBA{R: 255, G: 0, B: 0, A: 255} // Rojo
	}

	var pnlTitle = canvas.NewText(pnlTittleText, textColor)
	pnlTitle.TextStyle.Bold = true
	pnlTitle.TextSize = 30.0
	pnlTitle.Alignment = fyne.TextAlignCenter
	return pnlTitle
	//return container.NewHBox(pnlTitle)
	//return canvas.NewText(pnlText, textColor)
	//return widget.NewLabelWithStyle(pnlText, fyne.TextAlignCenter, fyne.TextStyle{Bold: false, Italic: false})
}
