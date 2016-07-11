/**
 * Created by dido on 7/10/16.
 */
import { Component} from '@angular/core';
import {ImageService} from '../services/image.service'


@Component({
        selector: 'my-search-images',
        templateUrl: 'app/template/images-search.component.html'
})
export class ImagesSearchComponent {
    submitted = false;
    sorting   = ['stars', 'pulls',];
    ordering  = ['ascending order','descending order'];
     
    bin :string = "python"
    version: string  = "3.3.6";
    sort: string;
    order : string;

    constructor( private imageService: ImageService){
    }
    
    searchImages(){
        this.imageService.searchImages('python=2')
    }

    onSubmit() {
        //this.searchImages(this.diagnostic)
        this.imageService.searchImages(this.diagnostic)
        this.submitted = true;
    }

     // TODO: Remove this when we're done
    get diagnostic() { return this.bin+"="+this.version }

}


// class SearchUrlEncoded{
//     bins = [{bin:String, ver:String}];
//
// }
