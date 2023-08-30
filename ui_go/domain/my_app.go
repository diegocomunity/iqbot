package domain

import ports "github.com/diegocomunity/iq/ui_go/internal/ports"

// MyApp es una aplicación que muestra un mensaje de bienvenida en la interfaz de usuario
type MyApp struct {
	ui ports.UI
}

// NewMyApp crea una nueva instancia de MyApp con una implementación de la interfaz de usuario
func NewMyApp(ui ports.UI) *MyApp {
	return &MyApp{
		ui: ui,
	}
}

// Run ejecuta la aplicación y muestra el mensaje de bienvenida
func (a *MyApp) Run() {
	// Lógica de negocio...
	//message := "¡Bienvenido a mi aplicación!"
	//a.ui.ShowWelcomeMessage(message)
	a.ui.ShowLogin()
}
