package service

import (
	"log"

	"github.com/diegocomunity/iq/ui_go/adapters/outbound/rpc"
)

// RPCService representa el servicio de dominio que utiliza el cliente RPC.
type RPCService struct {
	RPCClient *rpc.RPCClient
}

// Login realiza una llamada RPC para iniciar sesión en el servidor.
func (s *RPCService) Login(username, password string) ([]byte, error) {
	payload := `<?xml version="1.0"?>
		<methodCall>
			<methodName>login</methodName>
			<params>
				<param>
					<value><string>` + username + `</string></value>
				</param>
				<param>
					<value><string>` + password + `</string></value>
				</param>
			</params>
		</methodCall>`

	responseData, err := s.RPCClient.SendRequest(payload)
	if err != nil {
		log.Println("Error de inicio de sesión:", err)
		return nil, err
	}

	return responseData, nil
}
