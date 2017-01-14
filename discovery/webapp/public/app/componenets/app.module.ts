/**
 * Created by dido on 9/3/16.
 */
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent }   from './app.component';
import { FormsModule }   from '@angular/forms';
import { HttpModule }    from '@angular/http';

import {ImagesSearchComponent } from './images-search.component'
import {ImageService} from "../services/image.service";
import {Configuration} from "../app.constants";
import {ImagesComponent} from "./images.component";
import {ToMegabytes } from '../filters/to-megabytes.pipe';

import { routing } from '../routes/app.routes';
import {DashboardComponent} from "./dashboard.component";
import {SoftwareService} from "../services/software.service";



@NgModule({
  imports:      [
        BrowserModule,
        FormsModule,
        HttpModule,
        routing
],
  declarations: [
      AppComponent,
      DashboardComponent,
      ImagesSearchComponent,
      ImagesComponent,
      ToMegabytes
  ],
  providers: [
     ImageService,
      SoftwareService,
      Configuration,
  ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
