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

    <!--button class="btn-xs  btn-primary" (click)="goBack()"> <span class="glyphicon glyphicon-menu-left"></span>Dashboard</button-->


    <!--div [hidden]="!hideCount" >
    <div style="text-align:center">
       <img src="app/images/loader.gif" width="100px">
    </div-->


    <div  class="container-fluid">
        <div [hidden]="!hideCount" style="text-align:center">
          <img src="app/images/loader.gif" width="70px">
        </div>

        <div [hidden]="hideCount" style="text-align:center; color:#2d5699;font-size:20pt">

         <div>{{pager.count}} images found </div>

        <!-- pager-->
        <ul [hidden]="hideCount" style="font-size:14" class="pagination">
                <li [ngClass]="{disabled:pager.currentPage === 1}">
                    <a (click)="getPageImages(1)">First</a>
                </li>
                <li [ngClass]="{disabled:pager.currentPage === 1}">
                    <a (click)="getPageImages(pager.currentPage - 1)">Previous</a>
                </li>
                <li *ngFor="let page of pager.pages" [ngClass]="{active:pager.currentPage === page}">
                    <a (click)="getPageImages(page)">{{page}}</a>
                </li>
                <li [ngClass]="{disabled:pager.currentPage === pager.totalPages}">
                    <a (click)="getPageImages(pager.currentPage + 1)">Next</a>
                </li>
                <li [ngClass]="{disabled:pager.currentPage === pager.totalPages}">
                    <a (click)="getPageImages(pager.totalPages)">Last</a>
                </li>
          </ul>
        </div>

        <div class="row-image" *ngFor="let image of pager.pagedImages"  (click)="onSelect(image)">

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

    //count = 0;

    // array of all items to be paged
    //private allItems: any[];

    // pager object
    pager: any = {
      count :0,
      pagedimages: [],
      currentPage : 1,
    };

    // paged items
    //pagedItems: any[];


    constructor(
        private imageService: ImageService,
        private route: ActivatedRoute ) {
    }

    ngOnInit(): void {
      console.log (this.route.params)
        this.route.params.forEach((params: Params) => {
            //console.log(params);
            this.searchApi = params['parm'];
            this.getPageImages(1);
        });
    }

    getPageImages(page: number){
      console.log("submitted page: "+ page)
      if (page < 1 || page > this.pager.totalPages) {
            return;
      }
      this.imageService.searchImages(this.searchApi + "&page="+page)
          .then(resImages => {

              if (resImages.count > 0) {
                  //this.pagedImages = resImages.images;

                  this.pager.count = resImages.count;
                  this.pager.pagedImages =  resImages.images
                  this.pager.totalPages = resImages.pages;
                  this.pager.currentPage = page;
                  this.pager.pages = this.getIntermediatePages(resImages.pages, page);

                  this.hideCount = false;
                  console.log(resImages);
              }
              else{
                  this.pager.count = resImages.count;
                  this.hideCount = false;
              }
          });
    }


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

   getIntermediatePages(totalPages, currentPage){
      let startPage: number, endPage: number;
      if (totalPages <= 10) {
          // less than 10 total pages so show all
          startPage = 1;
          endPage = totalPages;
      } else {
          // more than 10 total pages so calculate start and end pages
          if (currentPage <= 6) {
              startPage = 1;
              endPage = 10;
          } else if (currentPage + 4 >= totalPages) {
              startPage = totalPages - 9;
              endPage = totalPages;
          } else {
              startPage = currentPage - 5;
              endPage = currentPage + 4;
          }
      }
      return this.range(startPage, endPage + 1)
    }

    range(start, end) {
      return Array(end - start + 1).fill().map((_, idx) => start + idx)
    }

    // range(start, count) {
    //      return Array.apply(0, Array(count))
    //        .map(function (element, index) {
    //          return index + start;
    //      });
    //    };


}
