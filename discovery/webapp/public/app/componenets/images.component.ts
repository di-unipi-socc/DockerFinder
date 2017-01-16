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

        <!--div class="container">

        <!- -inti row "col-sm-6 col-md-4"- ->
          <div class="row">
            <div class="col-xs-12" *ngFor="let image of images"  [class.selected]="image === selectedImage" (click)="onSelect(image)">

              <div class="thumbnail">
              <span>
                <img src="app/images/docker.png" style="width:50px" alt="">
                <p class="reponame"  (click)="onSelect(image)"> {{image.name}} </p>
              </span>
                <div class="caption">

                  <!- -h4 class="reponame" (click)="onSelect(image)">{{image.name}} </h4- ->
                  <div class="details-image">
                    <span class="glyphicon glyphicon-star" aria-hidden="true"> </span> {{image.stars}} Star
                    <span class="glyphicon glyphicon-download" aria-hidden="true"></span>  {{image.pulls}}  Pulls
                    <span class="glyphicon glyphicon-save" aria-hidden="true"> </span>  {{image.size | toMegabytes }}MB
                  </div>

                  <div class="group-softwares">
                    <div class="row">  <!- -nested row- ->
                        <div class="col-md-3 col-sm-3 my-software"  *ngFor="let sw of image.softwares">
                           {{sw.software}} {{sw.ver}}
                        </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>  <!- -end row- ->
        </div-->
<!-- container fluid example-->
    <div  class="container-fluid">
        <div class="row-image" *ngFor="let image of images"  (click)="onSelect(image)">

            <img src="app/images/docker.png" style="width:70px" class="row-image-group" alt="">

            <div class="row-image-group">
              <h1 class="reponame"  (click)="onSelect(image)"> {{image.name}} </h1>
              <span class="glyphicon glyphicon-star" aria-hidden="true"> </span> {{image.stars}} Star
              <span class="glyphicon glyphicon-download" aria-hidden="true"></span>  {{image.pulls}}  Pulls
              <span class="glyphicon glyphicon-save" aria-hidden="true"> </span>  {{image.size | toMegabytes }}MB
              <div [hidden]="image.is_automated">automated build</div>
              <div> </div>
              <!--div ng-show="image.is_automated">Is automated</div-->
              <!--span [hidden]="!image.is_private">Public</span-->

            <div class="my-software row-image-group"  *ngFor="let sw of image.softwares">
                   {{sw.software}} {{sw.ver}}
            </div>
          </div>

        </div>
    </div>

    `,


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
        //this.selectedImage = image;
      //  name =
        var values = image.name.split(':');
        var repository = values[0];
        var tag = values[1];
        //console.log(repository)
        var url = "https://hub.docker.com/r/"+repository

        window.open(url)
    }

    gotoDetail() {
        //this.router.navigate(['/detail', this.selectedImage._id]);
    }
    goBack(): void {
        window.history.back();
    }
}
