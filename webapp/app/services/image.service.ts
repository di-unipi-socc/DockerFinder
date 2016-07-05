/**
 * Created by dido on 7/5/16.
 */
import { Injectable }     from '@angular/core';
import { Http, Response } from '@angular/http';

import { Observable }     from 'rxjs/Observable';

@Injectable()
export class ImageService {
  
  constructor (private http: Http) {}
  
  private imagesUrl = 'api/images';  // URL to web API

  getImages (): Observable<string[]> {
    return this.http.get(this.imagesUrl)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  private extractData(res: Response) {
    let body = res.json();
    return body.data || { };
  }

  private handleError (error: any) {
    // In a real world app, we might use a remote logging infrastructure
    // We'd also dig deeper into the error to get a better message
    let errMsg = (error.message) ? error.message :
      error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg); // log to console instead
    return Observable.throw(errMsg);
  }
}