/**
 * Created by dido on 7/5/16.
 */

import { Component }         from '@angular/core';
// Add the RxJS Observable operators we need in this app.
import '../rxjs-operators';

import { ImagesListComponent }        from './images-list.componenet';
import { ImageDetailComponent}        from './image-detail.component';
import {Image } from '../image';

@Component({
  selector: 'my-app',
  template: `
    <h1>DoFinder Images</h1>
    <ul class="images">
        <li *ngFor="let image of images"  [class.selected]="image === selectedImage" (click)="onSelect(image)"> 
           <span class="badge"> {{image.id}}</span> {{image.name}}
        </li>
    </ul>
    
    <my-image-detail [image]="selectedImage"></my-image-detail>
   
    <!--image-list></image-list-->
  `,
  styles: [`
      .selected {
        background-color: #CFD8DC !important;
        color: white;
      }
      .images {
        margin: 0 0 2em 0;
        list-style-type: none;
        padding: 0;
        width: 15em;
      }
      .images li {
        cursor: pointer;
        position: relative;
        left: 0;
        background-color: #EEE;
        margin: .5em;
        padding: .3em 0;
        height: 1.6em;
        border-radius: 4px;
      }
      .images li.selected:hover {
        background-color: #BBD8DC !important;
        color: white;
      }
      .images li:hover {
        color: #607D8B;
        background-color: #DDD;
        left: .1em;
      }
      .images .text {
        position: relative;
        top: -3px;
      }
      .images .badge {
        display: inline-block;
        font-size: small;
        color: white;
        padding: 0.8em 0.7em 0 0.7em;
        background-color: #607D8B;
        line-height: 1em;
        position: relative;
        left: -1px;
        top: -4px;
        height: 1.8em;
        margin-right: .8em;
        border-radius: 4px 0 0 4px;
      }
    `],

  directives: [
    ImageDetailComponent
  ]

})
export class AppComponent {
    //image : Image ={ id:1, name:'python'};
    selectedImage : Image;

    public images = IMAGES;

    //constructor( private imageService: ImageService)

    onSelect(image: Image){
        this.selectedImage = image;
    }
}


const IMAGES: Image[] = [
  { id: 11, name: 'java' },
  { id: 12, name: 'dido' },
  { id: 13, name: 'Bombasto' },
  { id: 14, name: 'Celeritas' },
  { id: 15, name: 'Magneta' },
  { id: 16, name: 'RubberMan' },
  { id: 17, name: 'Dynama' },
  { id: 18, name: 'Dr IQ' },
  { id: 19, name: 'Magma' },
  { id: 20, name: 'Tornado' }
];