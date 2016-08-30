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
    softwares : Software [] = [ new Software("", "", false)]; //{software:'', version:'', error:false}];
    msg: string = '';
    

    bin :string ;
    version: string;
    sort: string;
    order : string;

    resultImages : Image[];
    count = 0;

    constructor( private router: Router, private imageService: ImageService){
        //this.softwares.push(new Software("", ""));
    }

    remove(id: number) {
        this.softwares.splice(id, 1);
    }

    add(id){
        this.softwares.push(new Software(" ", " ", false));
    }

      change_version(item) {
        var regex = /^[1-9].([1-9].)*[1-9]$/g;
        if (!regex.test(item.version)){
          this.msg="The version syntax it is not correct!";
          item.error=true;
        }else{
          this.msg='';
          item.error=false;
        }
      }

    diagnostic() {
        var result  = "";
        for (var sw of this.softwares) {
            result += sw.name + "=" + sw.version;
        }
        return result;
    }

    onSubmit() {
        //this.constructSearchUrl();
        this.imageService.searchImages(this.constructSearchUrl())
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
        for(var sw of this.softwares){
            url_search+=sw.name+"="+sw.version+"&";
        }
        return url_search;
    }


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
