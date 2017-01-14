/**
 * Created by dido on 7/6/16.
 */
import {Component, OnInit, Input}         from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Image } from '../models/image';
import {ImageService} from "../services/image.service";



@Component({
    selector: 'my-images',
    //pipes:     [toMegabytes],
    template: `
        <button class="btn btn-primary"  (click)="goBack()">Back</button>
        <div class="container">
          <div class="row align-items-center">
            <div class="col-sm-6 col-md-4" *ngFor="let image of images"  [class.selected]="image === selectedImage" (click)="onSelect(image)">
              <div class="thumbnail">
                <div class="caption">
                  <h4 class="reponame" (click)="onSelect(image)">{{image.name}} </h4>
                  <div>
                    <span class="glyphicon glyphicon-star" aria-hidden="true"> </span> {{image.stars}} Star
                    <span class="glyphicon glyphicon-download" aria-hidden="true"></span>  {{image.pulls}}  Pulls
                    <span class="glyphicon glyphicon-save" aria-hidden="true"> </span>  {{image.size | toMegabytes }}MB
                  </div>
                  <span class="language" *ngFor="let sw of image.softwares" >
                       {{sw.software}} {{sw.ver}}, 
                  </span>
                </div>

              </div>
            </div>

            <!--table>
              <template ngFor #image [ngForOf]="images" #i="index">
                <template ngFor #sw [ngForOf]="image.softwares" #j="index">
                  <tr>{{sw.software}}</tr>
                </template>
              </template>
            </table-->
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
export class ImagesComponent implements OnInit {
    errorMessage: string;
    selectedImage: Image;

    @Input()
    images: Image[];
    count = 0;


    constructor(
        private imageService: ImageService,
        private route: ActivatedRoute) {
    }

    ngOnInit(): void {
        let searchApi;
        console.log(this.route.params);
        this.route.params.forEach((params: Params) => {
            console.log(params);
            searchApi = params['parm'];
            // let search= +params['id'];
            this.imageService.searchImages(searchApi)
                .then(resImages => {
                    if (resImages.length > 0) {
                        this.images = resImages;
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

    onSelect(image: Image) {
        this.selectedImage = image;
    }

    gotoDetail() {
        //this.router.navigate(['/detail', this.selectedImage._id]);
    }
    goBack(): void {
        window.history.back();
    }
}
