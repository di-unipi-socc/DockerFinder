/**
 * Created by dido on 7/6/16.
 */
import {Component, OnInit, Input}         from '@angular/core';
import { Router } from '@angular/router';

import {Image } from '../image';
import {ImageService} from "../services/image.service";



@Component({
  selector: 'my-images',
  template: `
    <h1>DoFinder Images</h1>
     <div *ngIf="images && images.length > 0">
       <p> Found images : {{images.length}} </p>
        <ul class="images">
            <li *ngFor="let image of images"  [class.selected]="image === selectedImage" (click)="onSelect(image)"> 
               <span class="badge"> {{image.stars}}</span> {{image.repo_name}}
            </li>
        </ul>
        <div *ngIf="selectedImage">
          <h2>
            {{selectedImage.repo_name | uppercase}} : {{selectedImage.description}}
          </h2>
          <button (click)="gotoDetail()">View Details</button>
        </div>
    </div>
    <div *ngIf="images && images.length == 0">
        Images not found
    </div>
    `,
  styleUrls: ['app/styles/images.component.css'],

})
export class ImagesComponent implements OnInit{
    errorMessage:string;
    selectedImage:Image;

    @Input()
    images:Image [];

    constructor(private router:Router,
                private imageService:ImageService) {
    }

     ngOnInit() {
        // this.getImages();
        //this.images =[]
    }
    //
    // getImages() {
    //     this.imageService.getImages().then(images => this.images = images)
    // }

    onSelect(image:Image) {
        this.selectedImage = image;
    }

    gotoDetail() {
        this.router.navigate(['/detail', this.selectedImage._id]);
    }

}