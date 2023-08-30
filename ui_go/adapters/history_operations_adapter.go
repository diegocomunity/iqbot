package adapters

import "github.com/diegocomunity/iq/ui_go/models"

type hisoryOperationsAdapter struct{}

func NewHistoryOperationsAdapter() *hisoryOperationsAdapter {
	return &hisoryOperationsAdapter{}
}

func (h *hisoryOperationsAdapter) GetHistoryOperations() []models.Operation {

	//acá se envia la solicitud al servidor y se obtienen el historial de operaciones
	return []models.Operation{
		{
			ID: "",
		},
	}
}
