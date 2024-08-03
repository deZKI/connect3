import {Component, OnInit} from '@angular/core';
import {ParticipantCardComponent} from "../../components/participant-card/participant-card.component";
import {Participant, User} from "../../shared/interfaces/user.interfaces";
import {NgForOf} from "@angular/common";
import {UserService} from "../../services/user.service";
import {take, tap} from "rxjs";

@Component({
  selector: 'app-participant',
  standalone: true,
  imports: [
    ParticipantCardComponent,
    NgForOf,
  ],
  templateUrl: './participant.component.html',
  styleUrl: './participant.component.scss'
})
export class ParticipantComponent implements OnInit {
  users: User[] = []

  constructor(private userService: UserService) {
  }

  ngOnInit() {
    this.userService.getUsers().pipe(
      take(1),
      tap(users => this.users = users)
    ).subscribe()
  }
}
