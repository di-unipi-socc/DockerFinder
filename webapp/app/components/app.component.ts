/**
 * Created by dido on 7/5/16.
 */
import { Component }       from '@angular/core';
import { ROUTER_DIRECTIVES } from '@angular/router';
import { ImageService}     from '../services/image.service'

// Add the RxJS Observable operators we need in this app.
//import './rxjs-operators';

@Component({
  selector: 'my-app',
    template: `
        <h1>{{title}}</h1>
        <nav>
            <a [routerLink]="['/dashboard']" routerLinkActive="active">Dashboard</a>
            <a [routerLink]="['/images']" routerLinkActive="active">Images</a>
         </nav>
         <router-outlet></router-outlet>
`,
    styleUrls: ['app/styles/app.component.css'],
    directives:[ROUTER_DIRECTIVES],
    providers: [
        ImageService
    ]

})
export class AppComponent{
     title = 'DoFinder Images';
}

