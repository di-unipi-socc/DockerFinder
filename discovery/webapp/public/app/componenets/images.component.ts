/**
 * Created by dido on 7/6/16.
 */
import {Component, OnInit, Input}         from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Image } from '../models/image';
import {ImageService} from "../services/image.service";



@Component({
  selector: 'my-images',
  template: `
        <button class="btn btn-primary"  (click)="goBack()">Back</button>
        <div class="row">
          <div class="col-sm-6 col-md-4" *ngFor="let image of images"  [class.selected]="image === selectedImage" (click)="onSelect(image)">
            <div class="thumbnail">
              <div class="caption">
                <h4 (click)="onSelect(image)">{{image.name}}</h4>
                <p><span class="badge">{{image.stars}}</span> Stars</p>
                <p><span class="badge">{{image.pulls}}</span> Pulls</p>
                <p><span class="badge">{{image.size}}</span> Size</p>

                <!--<p><a href="#" class="btn btn-primary" role="button">Button</a> <a href="#" class="btn btn-default" role="button">Button</a></p>-->
              </div>
            </div>
          </div>
        </div>
    <!--<h1>DoFinder Images</h1>
     <div *ngIf="images && images.length > 0">
       <p> Found images : {{images.length}} </p>
        <ul class="images">
            <li *ngFor="let image of images"  [class.selected]="image === selectedImage" (click)="onSelect(image)">
               <span class="badge"> {{image.stars}}</span> {{image.name}}
            </li>
        </ul>
        <div *ngIf="selectedImage">
          <h2>
            {{selectedImage.name | uppercase}} : {{selectedImage.description}}
          </h2>
          <button (click)="gotoDetail()">View Details</button>
        </div>
    </div>
    <div *ngIf="images && images.length == 0">
        Images not found
    </div>-->
    `,
 // styleUrls: ['app/styles/images.component.css'],

})
export class ImagesComponent implements OnInit{
    errorMessage:string;
    selectedImage:Image;

    @Input()
    images: Image [];
    count =0;


    constructor(
      private imageService: ImageService,
      private route: ActivatedRoute) {
    }

     ngOnInit():void {
         let searchApi;
           console.log(this.route.params);
        this.route.params.forEach((params: Params) => {
            console.log(params);
            searchApi = params['parm'];
        // let search= +params['id'];
         this.imageService.searchImages(searchApi)
            .then(resImages=>{
                if(resImages.length > 0 ) {
                    this.images= resImages;
                    this.count = resImages.length;
                    console.log(resImages);
                }
          });

  });
    }
    //
    // getImages() {
    //     this.imageService.getImages().then(images => this.images = images)
    // }

    onSelect(image:Image) {
        this.selectedImage = image;
    }

    gotoDetail() {
        //this.router.navigate(['/detail', this.selectedImage._id]);
    }
    goBack(): void {
      window.history.back();
    }
}
