import { Injectable } from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Participant, User, UserExtended, Speakers} from "../shared/interfaces/user.interfaces";

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private apiTeammates = `${environment.apiUrl}/teammates/`
  private apiUsers = `${environment.apiUrl}/users/`
  private apiSpeakers = `${environment.apiUrl}/speakers/`


  constructor(private http: HttpClient) {
  }

  getParticipants(): Observable<Participant[]> {
    return this.http.get<Participant[]>(this.apiTeammates);
  }

  getSpeakers(): Observable<Speakers[]> {
    return this.http.get<Speakers[]>(this.apiSpeakers);
  }


  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUsers);
  }


  getUserExtended(id: string): Observable<UserExtended> {
    return this.http.get<UserExtended>(this.apiUsers + id);
  }

}
