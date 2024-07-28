import { Injectable } from '@angular/core';
import {environment} from "../../enviroments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Participant} from "../shared/interfaces/user.interfaces";

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private apiBooks = `${environment.apiUrl}/participants/`

  constructor(private http: HttpClient) {
  }

  getParticipants(): Observable<Participant[]> {
    return this.http.get<Participant[]>(this.apiBooks);
  }

}
