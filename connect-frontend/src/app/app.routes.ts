import { Routes } from '@angular/router';
import {ParticipantComponent} from "./pages/participant/participant.component";
import {PostsComponent} from "./pages/posts/posts.component";
import {HomeComponent} from "./pages/home/home.component";

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'posts', component: PostsComponent },
  { path: 'participants', component: ParticipantComponent },
  { path: '**', redirectTo: '', pathMatch: 'full' } // редирект на главную страницу для неизвестных маршрутов
];
