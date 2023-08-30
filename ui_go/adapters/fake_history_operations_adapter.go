// fakeHistoryOperationsAdapter.go

package adapters

import (
	"math/rand"
	"time"

	"github.com/diegocomunity/iq/ui_go/models"
)

// fakeHistoryOperationsAdapter is an adapter that generates fake history of operations data.
type fakeHistoryOperationsAdapter struct{}

// NewFakeHistoryOperationsAdapter creates a new instance of fakeHistoryOperationsAdapter.
func NewFakeHistoryOperationsAdapter() *fakeHistoryOperationsAdapter {
	return &fakeHistoryOperationsAdapter{}
}

// GetHistoryOperations generates fake history of operations data for demonstration purposes.
func (f *fakeHistoryOperationsAdapter) GetHistoryOperations() []models.Operation {
	// Generate random data for the history of operations
	// For demonstration purposes, we're just creating random data here
	operations := make([]models.Operation, 10)
	for i := 0; i < len(operations); i++ {
		operations[i] = models.Operation{
			ID:     generateID(),
			Activo: generateActivo(),
			Tipo:   generateTipo(),
			Precio: generatePrecio(),
			PNL:    generatePNL(),
			Fecha:  generateFecha(),
		}
	}

	return operations
}

func generateID() string {
	// Implement your logic to generate a unique ID for each operation
	return "ID-" + randomString(6)
}

func generateActivo() string {
	// Implement your logic to generate a random asset for each operation
	activos := []string{"EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"}
	return activos[rand.Intn(len(activos))]
}

func generateTipo() string {
	// Implement your logic to generate a random operation type (Buy/Sell)
	tipos := []string{"Buy", "Sell"}
	return tipos[rand.Intn(len(tipos))]
}

func generatePrecio() float64 {
	// Implement your logic to generate a random price for each operation
	return rand.Float64()*100.0 + 1.0
}

func generatePNL() float64 {
	// Implement your logic to generate a random PNL (profit/loss) for each operation
	return rand.Float64()*200.0 - 100.0
}

func generateFecha() time.Time {
	// Implement your logic to generate a random date and time for each operation
	now := time.Now()
	daysAgo := rand.Intn(30)
	return now.AddDate(0, 0, -daysAgo)
}

// randomString generates a random alphanumeric string of given length.
func randomString(length int) string {
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	rand.Seed(time.Now().UnixNano())
	b := make([]byte, length)
	for i := range b {
		b[i] = charset[rand.Intn(len(charset))]
	}
	return string(b)
}
