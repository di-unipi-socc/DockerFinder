/**
 * Created by dido on 7/6/16.
 */
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Image } from '../image';
import { ImageService } from '../services/image.service';

import {ImagesSearchComponent} from './images-search.component'


@Component({
  selector: 'my-dashboard',
  templateUrl: 'app/template/dashboard.component.html',
  styleUrls: [`app/styles/dashboard.component.css`],
  directives:[ImagesSearchComponent]
})
export class DashboardComponent implements OnInit{

  images : Image[] = [];

  constructor(
      private imageService: ImageService,
      private router: Router) {
  }

  ngOnInit() {
      this.imageService.getImages()
          .then(images =>  this.images = images.slice(1, 5));
  }

  gotoDetail(image:Image) {
      let link = ['/detail', image._id];
      this.router.navigate(link);
  }

}
