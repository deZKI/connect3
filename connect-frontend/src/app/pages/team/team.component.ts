import {Component} from '@angular/core';
import {UserService} from "../../services/user.service";
import {take, tap} from "rxjs";
import {Participant} from "../../shared/interfaces/user.interfaces";
import {NgForOf} from "@angular/common";
import {ParticipantCardComponent} from "../../components/participant-card/participant-card.component";

@Component({
  selector: 'app-team',
  standalone: true,
  imports: [
    NgForOf,
    ParticipantCardComponent
  ],
  templateUrl: './team.component.html',
  styleUrl: './team.component.scss'
})
export class TeamComponent {
  participants: Participant[] = []

  constructor(private userService: UserService) {
  }

  ngOnInit() {
    this.userService.getParticipants().pipe(
      take(1),
      tap(participants => this.participants = participants)
    ).subscribe()
  }
}
