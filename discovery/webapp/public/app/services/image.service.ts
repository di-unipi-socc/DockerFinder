/**
 * Created by dido on 7/5/16.
 */
import { Injectable }     from '@angular/core';
import 'rxjs/add/operator/toPromise';  //for toPromise()

import { Image } from '../models/image';
import { Configuration } from '../app.constants';


import {Http,Response, URLSearchParams,Headers} from "@angular/http";
import {Observable} from "rxjs/Rx";

@Injectable()
export class ImageService {
  private imagesUrl :string;        //= 'http://127.0.0.1:8000/api/images'; //'app/images.json'
  private searchUrl = '/search?';     // 'http://127.0.0.1:8000/search?';
  private searchQueryString:string = ""; // the query string used ti restore the same view in the dashboard view
  private headers: Headers;


  constructor (private http: Http, private configuration:Configuration) {
      this.imagesUrl = configuration.ServerWithApiUrl;
        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
  }

//  getImages(): Promise<Image[]>{
  // getImages(page:number = 1): Promise<>{
  //      return this.http.get(this.imagesUrl+"&page="+page)
  //                   . toPromise()
  //                   .then(response => response.json())
  //                   // count: total number od images taht match the result
  //                   // pages: totalnumber of pages
  //                   // page:  the number
  //                   // limit: number of images per size
  //                   // images: array of images (currently)
  //                    //.then(response => response.json())//.data) as Image[])
  //                   .catch(this.handleError);
  // }

  // getImage(id:string){
  //       return this.getImages()
  //           .then(images => images.filter(image =>image._id === id)[0]);//[0]);===id
  //
  // }

  searchImages(queryString: string): Promise<any>{
      this.searchQueryString =  queryString
      return this.http.get(this.searchUrl + queryString)
          .toPromise()
          .then(response => response.json())
          .catch(this.handleError)

  }


  getTotalImages(): Promise<number>{
  return this.http.get("/images?total=true")
                   .toPromise()
                   .then(response => {
                     console.log(response.json()['count']);
                     return response.json()['count']; }
                    )
                   .catch(this.handleError);
  }

  getSearchQueryParameters(): URLSearchParams {
    let params = new URLSearchParams(this.searchQueryString);
    return params;
  }

  private extractData(res: Response) {
      let body = res.json();
      console.log(body);
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
