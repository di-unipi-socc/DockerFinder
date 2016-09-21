/**
 * Created by dido on 7/5/16.
 */
import { Injectable }     from '@angular/core';
import 'rxjs/add/operator/toPromise';  //for toPromise()

import { Image } from '../models/image';
import { Configuration } from '../app.constants';
// import { Image } from '../image';
// //import { IMAGES } from '../mock-images';
import {Http,Response, Headers} from "@angular/http";
import {Observable} from "rxjs/Rx";

@Injectable()
export class SoftwareService {
  private imagesUrl :string; //= 'http://127.0.0.1:8000/api/images'; //'app/images.json'
  private searchUrl = '/api/software?select=name';// http://127.0.0.1:3001/api/software?select=name;
  private headers: Headers;


  constructor (private http: Http, private configuration:Configuration) {
        this.imagesUrl = configuration.ServerWithApiUrl;
        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
  }

  getSoftware(): Promise<Image[]>{
    return this.http.get(this.imagesUrl)
                    . toPromise()
                     .then(response => response.json())//.data)
                     .catch(this.handleError);
  }

  getImage(id:string){
        return this.getImages()
            .then(images => images.filter(image =>image._id === id)[0]);//[0]);===id

  }

  searchImages(queryString: string): Promise<Image[]>{
      return this.http.get(this.searchUrl+queryString)
          .toPromise()
          .then(response => response.json().images)
          .catch(this.handleError)

  }

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