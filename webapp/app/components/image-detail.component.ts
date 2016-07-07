/**
 * Created by dido on 7/6/16.
 */
import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { ImageService } from '../services/image.service';
import { Image } from '../image';

@Component({
  selector: 'my-image-detail',
   template: `
    <div *ngIf="image">
      <h2>{{image.repo_name}} details!</h2>
      <div><label>id: </label>{{image._id}}</div>
      <div>
        <label>name: </label> {{image.repo_name}}
        <!--input [(ngModel)]="image.repo_name" placeholder="name"-->
      </div>
      <div><label>distro: </label>{{image.distro}} </div>
      <div><label>description: </label>{{image.description}} </div>
      <div><label>stars: </label>{{image.star_count}} </div>
      <div><label>pulls: </label>{{image.pull_count}} </div>
      <label>Binary:</label>
      <ul >
        <li *ngFor="let bins of image.bins"> 
          <label> name</label> {{bins.bin}} <label> ver </label> {{bins.ver}}
        </li>
     </ul>
     `,
    styleUrls:['app/styles/image-detail.component.css']
})
export class ImageDetailComponent implements OnInit, OnDestroy{
    // @Input() image: Image;  // [image] is an input property in ImageComponent ( tell what image to display selectedImage)
    // old implementation:
    // new : the image is not received bu the ImageComponent but the image is directly taken by the ImageDetailComponent
    // with the ImageService
    image : Image;
    sub: any;

    constructor(
      private imageService: ImageService,
      private route: ActivatedRoute) {
    }

    ngOnInit() {
        this.sub = this.route.params.subscribe(params => {
          let id = +params['id'];
          this.imageService.getImage(id)
            .then(image => this.image = image);
        });
      }

    ngOnDestroy() {
      this.sub.unsubscribe();
    }

    goBack() {
      window.history.back();
    }



}