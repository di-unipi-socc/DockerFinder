import { Component } from '@angular/core';
import {OnInit} from "@angular/core";

import {ImageService} from '../services/image.service';


@Component({
  selector: 'image-list',
  template: `
    <h1>Tour of Heroes ({{mode}})</h1>
        <h3>Heroes:</h3>
        <ul>
          <li *ngFor="let image of images">
            {{image.repo_name}}
          </li>
        </ul>
        New hero name:
        
    <div class="error" *ngIf="errorMessage">{{errorMessage}}</div>`,
  //directives: [HeroCardComponent, HeroEditorComponent]
})
export class ImagesListComponent implements OnInit{

    errorMessage: string;
    images : string[];
    mode : 'Observable';

    constructor (private imageService: ImageService) {}

    ngOnInit():any {
        this.getImages();
    }

    getImages(){
        this.imageService.getImages()
            .subscribe(images=> this.images = images,
            error => this.errorMessage = error)
    }
}