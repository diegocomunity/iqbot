package models

import "time"

type Operation struct {
	ID        string
	Activo    string
	Tipo      string
	Precio    float64
	Resultado float64
	PNL       float64
	Fecha     time.Time
}
