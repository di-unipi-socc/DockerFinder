/**
 * Created by dido on 7/10/16.
 */
import { Component} from '@angular/core';
import {ImageService} from '../services/image.service'
import {SoftwareService} from '../services/software.service'
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
    sorting  = [{name:'Ascending stars', val:"stars"},{name:'Descending stars',val:"-stars"}, 
        {name:'Ascending pulls', val:"pulls"},{name:'Descending pulls',val:"-pulls"},
        {name:'Ascending stars  Ascending pulls', val:"-stars -pulls"}
    ];

    comparisons = [{name:"Greater than", val:"_gt"},{name:"Less than",val:"_lt"},{name:"Equal",val:""}];


    softwares : Software [] = [ new Software("", "", false)]; //{software:'', version:'', error:false}];
    msg: string = '';

    selectedSort = {name:"sort", val:""};

    sizeCmpValue =  {name:"size",  cmp: this.comparisons[0].val, val:"0"};  //size_gt=x, size_lt=y, size=z
    pullsCmpValue = {name:"pulls", cmp: this.comparisons[0].val, val:"0"};
    starsCmpValue = {name:"stars", cmp: this.comparisons[0].val, val:"0"};

    
    availableSoftware : string [] =["java", "python", "wget"];

    resultImages : Image[];
    count = 0;

    constructor( private router: Router, private imageService: ImageService){//}, private softwareService: SoftwareService){
         //this.softwares.push(new Software("", ""));
          this.selectedSort.val = this.sorting[0].val;
    }


    callSearchApi(){
        let searchUrl = this.constructSearchUrl();
        //let link = ['/images', { this.selectedSort.name : this.selectedSort.val}];
        this.router.navigate(['/images'],{ queryParams: { sort: this.selectedSort.val}});
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

        return this.constructSearchUrl()
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
            url_search += sw.name+"="+sw.version+"&";
        }
        url_search += "sort="+this.selectedSort.val;
        url_search += "&"+this.sizeCmpValue.name+this.sizeCmpValue.cmp+"="+this.sizeCmpValue.val;
        url_search += "&"+this.pullsCmpValue.name+this.pullsCmpValue.cmp+"="+this.pullsCmpValue.val;
        url_search += "&"+this.starsCmpValue.name+this.starsCmpValue.cmp+"="+this.starsCmpValue.val;

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
