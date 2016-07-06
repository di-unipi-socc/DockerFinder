/**
 * Created by dido on 7/5/16.
 */
import { Injectable }     from '@angular/core';

import { Image } from '../image';
import { IMAGES } from '../mock-images';

@Injectable()
export class ImageService {
  
  constructor () {}
  
  private imagesUrl = 'api/images';  // URL to web API

  getImages (){
     return Promise.resolve(IMAGES);
    //return IMAGES;
    // return this.http.get(this.imagesUrl)
    //                 .map(this.extractData)
    //                 .catch(this.handleError);
  }

  getImage(id:number){
        return this.getImages()
            .then(images => images.filter(image => image.id === id)[0]);
    //   return this.getImages().filter(image => image.id === id)[0];

  }
  
  getImagesSlow (){
     return  new Promise<Image[]>(resolve => setTimeout(() => resolve(IMAGES), 4000)); //resolbe iamges after 4 seconds
    // return this.http.get(this.imagesUrl)
    //                 .map(this.extractData)
    //                 .catch(this.handleError);
  }
    
}