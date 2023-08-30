package ports

import "github.com/diegocomunity/iq/ui_go/models"

// HistoryOperationsPort defines the history operations port
type HistoryOperationsPort interface {
	GetHistoryOperations() []models.Operation
}
