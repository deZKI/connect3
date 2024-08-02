export interface Participant {
  id: number
  name: string
  surname: string
  inspiration: string
  photo: string
}

export interface User {
  id: number
  name: string
  surname: string
  photo: string
}


export interface UserExtended extends User{
  about_me: string,
  church: string,
  birth_date: string
}
