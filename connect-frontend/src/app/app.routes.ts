import {Routes} from '@angular/router';
import {ParticipantComponent} from "./pages/participant/participant.component";
import {PostsComponent} from "./pages/posts/posts.component";
import {HomeComponent} from "./pages/home/home.component";
import {SpeakersComponent} from "./pages/speakers/speakers.component";
import {TeamComponent} from "./pages/team/team.component";
import {ArchieveComponent} from "./pages/archieve/archieve.component";

export const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'speakers', component: SpeakersComponent},
  {path: 'team', component: TeamComponent},
  {path: 'participants', component: ParticipantComponent},
  {path: 'posts', component: PostsComponent},
  {path: 'archive', component: ArchieveComponent},
  {path: '**', redirectTo: '', pathMatch: 'full'} // редирект на главную страницу для неизвестных маршрутов
];
