import 'leaflet'

declare module 'leaflet' {
  namespace Draw {
    namespace Event {
      const CREATED: string
      const EDITED: string
      const DELETED: string
      const DRAWSTART: string
      const DRAWSTOP: string
      const EDITSTART: string
      const EDITSTOP: string
      const DELETESTART: string
      const DELETESTOP: string
    }
  }
}
