package events

import "github.com/podhmo/familiar/app/gen"

// GistCreated :
type GistCreated struct {
	Files []gen.Filename `json:"files"`
}
