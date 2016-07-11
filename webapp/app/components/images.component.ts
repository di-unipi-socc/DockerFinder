/**
 * Created by dido on 7/6/16.
 */
import { Component ,OnInit }         from '@angular/core';
import { Router } from '@angular/router';

import {Image } from '../image';
import {ImageService} from "../services/image.service";



@Component({
  selector: 'my-images',
  template: `
    <h1>DoFinder Images</h1>
    <ul class="images">
        <li *ngFor="let image of images"  [class.selected]="image === selectedImage" (click)="onSelect(image)"> 
           <span class="badge"> {{image.star_count}}</span> {{image.repo_name}}
        </li>
    </ul>
    <div *ngIf="selectedImage">
      <h2>
        {{selectedImage.repo_name | uppercase}} : {{selectedImage.description}}
      </h2>
      <button (click)="gotoDetail()">View Details</button>
    </div>
    `,
  styleUrls: ['app/styles/images.component.css'],

})
export class ImagesComponent implements OnInit {
    errorMessage:string;
    selectedImage:Image;
    images:Image [];

    constructor(private router:Router,
                private imageService:ImageService) {
    }

    ngOnInit() {
        this.getImages();
    }

    getImages() {
        // this.imageService.getImagesObservable().subscribe(
        //     images => this.images = images,
        //     error =>  this.errorMessage = <any>error)
        //

        this.imageService.getImages().then(images => this.images = images)
    }

    onSelect(image:Image) {
        this.selectedImage = image;
    }

    gotoDetail() {
        this.router.navigate(['/detail', this.selectedImage._id]);
    }

}