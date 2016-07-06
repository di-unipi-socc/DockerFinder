/**
 * Created by dido on 7/5/16.
 */
import { Injectable }     from '@angular/core';
import 'rxjs/add/operator/toPromise';  //for toPromise()

import { Image } from '../image';
//import { IMAGES } from '../mock-images';
import {Http,Response} from "@angular/http";
import {Observable} from "rxjs/Rx";

@Injectable()
export class ImageService {
  private imagesUrl = 'app/images.json';
  
  constructor (private http: Http) {}

  getImages(): Promise<Image[]>{
     //return Promise.resolve(IMAGES);
    //return IMAGES;
    return this.http.get(this.imagesUrl)
                    .toPromise()
                     .then(response => response.json())//.data)
                     .catch(this.handleError);
  }

  getImage(id:number){
        return this.getImages()
            .then(images => images.filter(image =>image._id === id)[0]);
        //return this.getImages().filter(image => image.id === id)[0];

  }
  
  // getImagesSlow (){
  //    return  new Promise<Image[]>(resolve => setTimeout(() => resolve(IMAGES), 4000));
  // }

    private extractData(res: Response) {
        let body = res.json();
        console.log(body)
        return body || { };
      }

     private handleError (error: any) {
    // In a real world app, we might use a remote logging infrastructure
    // We'd also dig deeper into the error to get a better message
    let errMsg = (error.message) ? error.message : error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg); // log to console instead
    return Observable.throw(errMsg);
  }
}