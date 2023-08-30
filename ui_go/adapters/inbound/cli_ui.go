package inbound

import "fmt"

// CLUI es una implementación de la interfaz UI utilizando la CLI
type CLUI struct{}

func NewCLUI() *CLUI {
	return &CLUI{}
}

// ShowWelcomeMessage muestra el mensaje de bienvenida en la CLI
func (ui *CLUI) ShowWelcomeMessage(message string) {
	fmt.Println(message)
}
