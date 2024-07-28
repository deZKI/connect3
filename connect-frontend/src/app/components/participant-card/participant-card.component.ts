import {Component, Input} from '@angular/core';
import {Participant} from "../../shared/interfaces/user.interfaces";

@Component({
  selector: 'app-participant-card',
  standalone: true,
  imports: [],
  templateUrl: './participant-card.component.html',
  styleUrl: './participant-card.component.scss'
})
export class ParticipantCardComponent {
  @Input() participant!: Participant
}
