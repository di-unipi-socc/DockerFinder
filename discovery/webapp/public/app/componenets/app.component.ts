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
`,
})
export class AppComponent {
  title = 'DockerFinder';
  subtitle = "Multi-attribute search of Docker images"


}
