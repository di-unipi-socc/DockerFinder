/**
 * Created by dido on 7/6/16.
 */
import { Component, Input } from '@angular/core';
import {Image } from '../image';

@Component({
  selector: 'my-image-detail',
   template: `
    <div *ngIf="image">
      <h2>{{image.name}} details!</h2>
      <div><label>id: </label>{{image.id}}</div>
      <div>
        <label>name: </label>
        <input [(ngModel)]="image.name" placeholder="name">
      </div>
     </div>`
})
export class ImageDetailComponent {
    @Input()
    image: Image;  //is an input property, AppComponent tell what image to display (selectedImage)
}