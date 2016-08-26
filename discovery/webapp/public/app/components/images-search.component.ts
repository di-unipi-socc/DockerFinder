/**
 * Created by dido on 7/10/16.
 */
import { Component} from '@angular/core';
import {ImageService} from '../services/image.service'
import {Image }  from '../models/image'
import {Software }  from '../models/software'
import {ImagesComponent}  from '../components/images.component'
import {Router} from "@angular/router";

@Component({
        selector: 'my-search-images',
        templateUrl: 'app/template/images-search.component.html',
        directives:[ImagesComponent]
})
export class ImagesSearchComponent {
    submitted = false;
    sorting   = ['stars', 'pulls',];
    ordering  = ['ascending order','descending order'];
    
    softwares:Software[] = [
        new Software("python", "3.4"),
        new Software("java", "1.9")

    ]; // = ['java', 'python', 'ruby', 'curl'];


    //sw = new Software("java", "1.9");

    bin :string ;
    version: string;
    sort: string;
    order : string;

    resultImages : Image[];
    count = 0;

    constructor( private router: Router, private imageService: ImageService){
       // this.softwares.push(new Software("java", "1.9"));
    }

    onSubmit() {
        this.constructSearchUrl();
        this.imageService.searchImages(this.diagnostic)
            .then(images=>{
                if(images.length > 0 ) {
                    this.resultImages = images;
                    this.count = images.length;
                    console.log(images);
                }
            });   //res in the json
        this.submitted = true;
        //this.router.navigate(['/images']);
    }

    constructSearchUrl(){
        var url_search ="";
        for(sw of this.softwares){
            url_search+=sw.name+"="+sw.version;
        }
        console.log(url_search)
    }

     // TODO: Remove this when we're done
    get diagnostic() { return this.bin+"="+this.version }

    edit(){
        this.submitted=false;
        this.resultImages = [];
    }

    addSoftware(){
        this.softwares.push(new Software("",""))
    }

}


// class SearchUrlEncoded{
//     bins = [{bin:String, ver:String}];
//
// }
