import {Component, OnInit} from '@angular/core';
import {NgForOf} from "@angular/common";
import {ParticipantCardComponent} from "../../components/participant-card/participant-card.component";
import {Speakers} from "../../shared/interfaces/user.interfaces";
import {UserService} from "../../services/user.service";
import {take, tap} from "rxjs";

@Component({
  selector: 'app-speakers',
  standalone: true,
    imports: [
        NgForOf,
        ParticipantCardComponent
    ],
  templateUrl: './speakers.component.html',
  styleUrl: './speakers.component.scss'
})
export class SpeakersComponent implements OnInit {
  speakers: Speakers[] = []

  constructor(private userService: UserService) {
  }

  ngOnInit() {
    this.userService.getSpeakers().pipe(
      take(1),
      tap(participants => this.speakers = participants)
    ).subscribe()
  }
}
