/**
 * Created by dido on 7/5/16.
 */
import { Component }       from '@angular/core';
import { ROUTER_DIRECTIVES } from '@angular/router';
import { ImageService}     from '../services/image.service'


@Component({
  selector: 'my-app',
    template: `
        <h1>{{title}}</h1>
        <nav>
            <a [routerLink]="['/dashboard']" routerLinkActive="active">Dashboard</a>
            <a [routerLink]="['/images']" routerLinkActive="active">Heroes</a>
         </nav>
         <router-outlet></router-outlet>
`,
    directives:[ROUTER_DIRECTIVES],
    providers: [
        ImageService
    ]

})
export class AppComponent{
     title = 'DoFinder Images';
}

