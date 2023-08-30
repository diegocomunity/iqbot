package inbound

import (
	"errors"
	"image/color"
	"log"
	"regexp"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
	"github.com/diegocomunity/iq/ui_go/adapters"
	"github.com/diegocomunity/iq/ui_go/adapters/outbound/rpc"
	"github.com/diegocomunity/iq/ui_go/domain/service"
)

// NewFyneUI crea una nueva instancia de FyneUI

// FyneUI es una implementación de la interfaz de usuario utilizando el framework Fyne
type fyneUI struct {
	app fyne.App
	win fyne.Window
}

// NewFyneUI crea una nueva instancia de FyneUI
func NewFyneUI() *fyneUI {

	return &fyneUI{
		app: app.New(),
	}
}

// ShowWelcomeMessage muestra el mensaje de bienvenida utilizando el framework Fyne
func (u *fyneUI) ShowWelcomeMessage(message string) {
	w := u.app.NewWindow("IQBot")
	w.Resize(fyne.NewSize(400, 600))

	tabs := widget.NewMenu(fyne.NewMenu("Broker", fyne.NewMenuItem("foo", func() { println("RUNTIME") }), fyne.NewMenuItemSeparator(), fyne.NewMenuItem("ACCION", func() { println(("hello world")) })))

	tabs2 := widget.NewAccordion(widget.NewAccordionItem("Tipo de mercado", canvas.NewText("MORE", color.NRGBA{200, 100, 123, 230})), widget.NewAccordionItem("ILove", canvas.NewText("Matilde", color.NRGBA{10, 123, 210, 155})))
	content := container.NewVBox(tabs2, tabs, widget.NewLabel(message))
	w.SetContent(content)

	w.ShowAndRun()
}

func (u *fyneUI) ShowLogin() {
	/*configuración inicial*/
	w := u.app.NewWindow("IQBot")
	w.Resize(fyne.NewSize(400, 600))

	//servicios necesarios para enviar al servidor y decodificar la respuesta xml
	rpcClient := &rpc.RPCClient{
		ServerURL: "http://localhost:8000/",
	}
	rpcService := &service.RPCService{
		RPCClient: rpcClient,
	}

	xmlAdapter := adapters.NewXMLAdapter()
	/*entradas de usuario*/
	emailEntry := widget.NewEntry()
	emailEntry.SetPlaceHolder("Email")
	emailEntry.Validator = validateEmail
	passwordEntry := widget.NewPasswordEntry()
	passwordEntry.SetPlaceHolder("Password")
	passwordEntry.Validator = validatePassword
	loginButton := widget.NewButton("Iniciar sesión", func() {
		email := emailEntry.Text
		password := passwordEntry.Text
		//validar los datos de entrada:

		// Validar los campos de entrada
		if err := validateEmail(email); err != nil {
			dialog.ShowError(err, w)
			return
		}
		if err := validatePassword(password); err != nil {
			dialog.ShowError(err, w)
			return
		}
		//end validación

		//enviar los datos al servidor
		responseData, err := rpcService.Login(email, password)

		if err != nil {
			log.Println("Error de inicio de sesión:", err)
			return
		}

		status, message, err := xmlAdapter.DecodeResponse(responseData)
		if err != nil {
			log.Println("Error al decodificar la respuesta del servidor:", err)
			return
		}
		if status == "error" {
			err := errors.New(message)
			dialog.ShowError(err, w)
			return
		}
		if status == "success" {
			dashboard := adapters.NewDashboardAdapter()

			dashboard.ShowDashboard()
			w.Close()
			return
		}

	})

	content := container.NewVBox(
		// Resto de los widgets de la ventana de login
		widget.NewLabel("Email"),
		emailEntry,
		widget.NewLabel("Password"),
		passwordEntry,
		loginButton,
	)
	w.SetContent(content)
	w.ShowAndRun()
}

func validateEmail(email string) error {
	// Expresión regular para validar el formato del correo electrónico
	emailRegex := `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

	// Validamos el correo electrónico con la expresión regular
	valid := regexp.MustCompile(emailRegex).MatchString(email)
	if !valid {
		return errors.New("Correo electrónico inválido")
	}

	return nil
}

func validatePassword(password string) error {
	if password == "" {
		return errors.New("La contraseña no puede estar vacía")
	}
	return nil
}

func ShowDashboard() {

}
