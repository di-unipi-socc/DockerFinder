/**
 * Created by dido on 9/3/16.
 */
import { Component } from '@angular/core';
import {ImageService} from "../services/image.service";



@Component({
  selector: 'my-app',
  template: `
      <div class="my-title">
        <h1 >{{title}} </h1>
        <h3>{{subtitle}} </h3>

      </div>
        <!--nav>
            <a [routerLink]="['/dashboard']" routerLinkActive="active">Dashboard</a>
            <a [routerLink]="['/images']" routerLinkActive="active">Images</a>
         </nav-->
      <router-outlet></router-outlet>

    <footer>
    <div class="my-footer">
     <!--address><a href="mailto:davide.neri@di.unipi.it">Davide Neri</a></address-->
      <a href="https://github.com/di-unipi-socc/DockerFinder" target="_blank">
     <img alt="DockerFinder GitHub Repository" src="app/images/github-mark.png" width="70px">
     </a>

      <a href="https://github.com/di-unipi-socc" target="_blank">
      <img alt="GitHubRepository" src="app/images/socc.png" width="40px">
      </a>
     </div>
    </footer>

`,
})
export class AppComponent {
  title = 'DockerFinder';
  subtitle = "Multi-attribute search of Docker images"

}
