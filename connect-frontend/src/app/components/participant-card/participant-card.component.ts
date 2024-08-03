import {Component, Input} from '@angular/core';
import {Participant, User} from "../../shared/interfaces/user.interfaces";

@Component({
  selector: 'app-participant-card',
  standalone: true,
  imports: [],
  templateUrl: './participant-card.component.html',
  styleUrl: './participant-card.component.scss'
})
export class ParticipantCardComponent {
  @Input() name!: string
  @Input() surname!: string
  @Input() inspiration!: string
  @Input() photo!: string
}
