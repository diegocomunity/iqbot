package rpc

import (
	"bytes"
	"io/ioutil"
	"log"
	"net/http"
)

// RPCClient representa el cliente RPC para enviar solicitudes al servidor.
type RPCClient struct {
	ServerURL string
}

// SendRequest envía una solicitud RPC al servidor.
func (c *RPCClient) SendRequest(payload string) ([]byte, error) {
	resp, err := http.Post(c.ServerURL, "text/xml", bytes.NewBufferString(payload))
	if err != nil {
		log.Fatal("Error al realizar la solicitud HTTP:", err)
		return nil, err
	}
	defer resp.Body.Close()

	responseData, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal("Error al leer la respuesta HTTP:", err)
		return nil, err
	}

	return responseData, nil
}
