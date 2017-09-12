package events

import (
	"fmt"
)

// EventType :
type EventType string

const (
	// EventTypeGistCreated :
	EventTypeGistCreated = EventType("gistCreated")
)

// String : stringer implementation
func (e EventType) String() string {
	switch e {
	case EventTypeGistCreated:
		return "gistCreated"
	default:
		panic(fmt.Sprintf("unexpected EventType %s, in string()", string(e)))
	}

}

// ParseEventType : parse
func ParseEventType(e string) EventType {
	switch e {
	case "gistCreated":
		return EventTypeGistCreated
	default:
		panic(fmt.Sprintf("unexpected EventType %v, in parse()", e))
	}

}
