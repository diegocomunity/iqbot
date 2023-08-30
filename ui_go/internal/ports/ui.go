package ports

// UI representa la interfaz de usuario abstraída
type UI interface {
	ShowLogin()
	ShowWelcomeMessage(message string)
}
