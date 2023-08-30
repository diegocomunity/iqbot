package adapters

import (
	"encoding/xml"
)

type XMLAdapter interface {
	DecodeResponse(responseData []byte) (string, string, error)
}

type xmlAdapter struct{}

func NewXMLAdapter() XMLAdapter {
	return &xmlAdapter{}
}

type MethodResponse struct {
	Params Params `xml:"params"`
}

type Params struct {
	Param Param `xml:"param"`
}

type Param struct {
	Value Value `xml:"value"`
}

type Value struct {
	Struct Struct `xml:"struct"`
	String string `xml:"string"`
}

type Struct struct {
	Members []Member `xml:"member"`
}

type Member struct {
	Name  string `xml:"name"`
	Value Value  `xml:"value"`
}

func (a *xmlAdapter) DecodeResponse(responseData []byte) (string, string, error) {
	var response MethodResponse
	if err := xml.Unmarshal(responseData, &response); err != nil {
		return "", "", err
	}

	status := ""
	message := ""

	for _, member := range response.Params.Param.Value.Struct.Members {
		switch member.Name {
		case "status":
			status = member.Value.String
		case "message":
			message = member.Value.String
		}
	}

	return status, message, nil
}
