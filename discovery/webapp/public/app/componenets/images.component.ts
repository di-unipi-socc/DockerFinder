/**
 * Created by dido on 7/6/16.
 */
import {Component, OnInit, Input}         from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Image } from '../models/image';
import {ImageService} from "../services/image.service";

import {PagerService } from '../services/pager.service';


//import * as _ from 'underscore';

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

        <div [hidden]="hideCount" style="text-align:center; color:#2d5699;font-size:20pt"> {{count}} images found !!!</div>

        <!-- pager-->
        <ul [hidden]="hideCount" class="pagination">
                <li [ngClass]="{disabled:pager.currentPage === 1}">
                    <a (click)="setPage(1)">First</a>
                </li>
                <li [ngClass]="{disabled:pager.currentPage === 1}">
                    <a (click)="setPage(pager.currentPage - 1)">Previous</a>
                </li>
                <li *ngFor="let page of pager.pages" [ngClass]="{active:pager.currentPage === page}">
                    <a (click)="setPage(page)">{{page}}</a>
                </li>
                <li [ngClass]="{disabled:pager.currentPage === pager.totalPages}">
                    <a (click)="setPage(pager.currentPage + 1)">Next</a>
                </li>
                <li [ngClass]="{disabled:pager.currentPage === pager.totalPages}">
                    <a (click)="setPage(pager.totalPages)">Last</a>
                </li>
          </ul>

        <div class="row-image" *ngFor="let image of pagedImages"  (click)="onSelect(image)">

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
    pagedImages: Image[];

    count = 0;

    // array of all items to be paged
    //private allItems: any[];

    // pager object
    pager: any = {
      currentPage : 1,
      pageSize: 10
    };

    // paged items
    //pagedItems: any[];


    constructor(
        private imageService: ImageService,
        private route: ActivatedRoute,
        private pagerService: PagerService  ) {
    }

    ngOnInit(): void {
        this.route.params.forEach((params: Params) => {
            //console.log(params);
            this.searchApi = params['parm'];

        //    this.searchApi + "&page="+ 1;
            // let search= +params['id'];
            this.imageService.searchImages(this.searchApi+ "&page="+ 1)
                .then(resImages => {
                    //console.log(resImages);
                    //count,pages,page, limit, images =[list of images]
                    if (resImages.count > 0) {
                        this.pagedImages = resImages.images;

                        this.count = resImages.count;

                        this.pager.totalPages = resImages.pages
                        this.pager.pages = this.getIntermediatePages(resImages.pages, this.pager.currentPage)

                        this.hideCount = false;
                        console.log(resImages);
                    }
                    else{
                        this.count = resImages.count;
                        this.hideCount = false;
                    }
                });

        });
    }

    setPage(page: number){
      console.log("submitted page: "+ page)
      if (page < 1 || page > this.pager.totalPages) {
            return;
      }
      //this.searchApi + "&page="+page;
      // let search= +params['id'];
      this.imageService.searchImages(this.searchApi + "&page="+page)
          .then(resImages => {
              if (resImages.count > 0) {
                  this.pagedImages = resImages.images;
                    this.pager.totalPages = resImages.pages;
                    this.pager.currentPage = page;
                      this.pager.pages = this.getIntermediatePages(resImages.pages, page);


                  this.hideCount = false;
                  console.log(resImages);
              }
              else{
                  this.count = resImages.count;
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

    range(start, count) {
         return Array.apply(0, Array(count))
           .map(function (element, index) {
             return index + start;
         });
       };


}
