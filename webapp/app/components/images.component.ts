/**
 * Created by dido on 7/6/16.
 */
import { Component ,OnInit }         from '@angular/core';
import { Router } from '@angular/router';

import {Image } from '../image';
import {ImageService} from "../services/image.service";

import { ImageDetailComponent}        from './image-detail.component';


@Component({
  selector: 'my-images',
  template: `
    <h1>DoFinder Images Component</h1>
    <ul class="images">
        <li *ngFor="let image of images"  [class.selected]="image === selectedImage" (click)="onSelect(image)"> 
           <span class="badge"> {{image.id}}</span> {{image.name}}
        </li>
    </ul>
    <div *ngIf="selectedImage">
      <h2>
        {{selectedImage.name | uppercase}} is my hero
      </h2>
      <button (click)="gotoDetail()">View Details</button>
    </div>
    `,

  styleUrls: ['app/styles/images.component.css'],

})
export class ImagesComponent implements OnInit{
    
    selectedImage : Image;
    images: Image [];

    constructor(
          private router: Router,
          private imageService: ImageService){}

    ngOnInit(){
         this.getImages();
    }

    getImages(){
       this.imageService.getImages().then(images => this.images = images)
        //this.images = this.imageService.getImages();
       // this.imageService.getImagesSlow().then(images => this.images = images)
    }

    onSelect(image: Image){
        this.selectedImage = image;
    }

    gotoDetail() {
        this.router.navigate(['/detail', this.selectedImage.id]);
    }
}