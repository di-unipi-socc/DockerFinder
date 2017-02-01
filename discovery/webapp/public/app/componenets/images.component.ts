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

    <button class="btn-xs  btn-primary" (click)="goBack()"> <span class="glyphicon glyphicon-menu-left"></span>Dashboard</button>


    <!--div [hidden]="!hideCount" >
    <div style="text-align:center">
       <img src="app/images/loader.gif" width="100px">
    </div-->


    <div  class="container-fluid">
        <div style="text-align:center">
          <img src="app/images/loader.gif" width="70px">
        </div>

        <div [hidden]="hideCount" style="text-align:center; color:#2d5699;font-size:20pt"> {{count}} images found</div>

        <div class="row-image" *ngFor="let image of images"  (click)="onSelect(image)">

            <img src="app/images/docker.png" style="width:70px" class="row-image-group" alt="">

            <div class="row-image-group">
              <h1 class="reponame"  (click)="onSelect(image)"> {{image.name}} </h1>
              <span class="glyphicon glyphicon-star" aria-hidden="true"> </span> {{image.stars}} Star
              <span class="glyphicon glyphicon-download" aria-hidden="true"></span>  {{image.pulls}}  Pulls
              <span class="glyphicon glyphicon-save" aria-hidden="true"> </span>  {{image.size | toMegabytes }}MB
              <!--div [hidden]="image.is_automated">automated build</div-->
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
    hideCount: boolean = true;
    searchApi: string;
    //showLoading:boolean =  True;

    @Input()
    images: Image[];
    count = 0;


    constructor(
        private imageService: ImageService,
        private route: ActivatedRoute) {
    }

    ngOnInit(): void {

        this.route.params.forEach((params: Params) => {
            //console.log(params);
            this.searchApi = params['parm'];
            // let search= +params['id'];
            this.imageService.searchImages(this.searchApi)
                .then(resImages => {
                    if (resImages.count > 0) {
                        this.images = resImages.images;
                        this.count = resImages.count;

                        this.hideCount = false;
                        console.log(resImages);
                    }
                    else{
                        this.count = 0
                        this.hideCount = false;
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
        console.log("going back with", this.searchApi )
      //  let link = ['/dockerfinder', this.constructSearchUrl()];
        //this.router.navigate(link);
    }
}
