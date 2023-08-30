package main

import (
	"github.com/diegocomunity/iq/ui_go/adapters/inbound"
	"github.com/diegocomunity/iq/ui_go/domain"
)

func main() {
	ui := inbound.NewFyneUI()
	//cli := inbound.NewCLUI()
	my_app := domain.NewMyApp(ui)
	my_app.Run()
}
