/**
 * Created by dido on 7/10/16.
 */
import { Component, Input } from '@angular/core';

import {ImageService} from '../services/image.service'
import {SoftwareService} from '../services/software.service'

import {Image }  from '../models/image'
import {Software }  from '../models/software'

// import {ImagesComponent}  from '../components/images.component'
import {Router} from "@angular/router";

@Component({
        selector: 'my-search-images',
        templateUrl: 'app/template/images-search.component.html',

})
export class ImagesSearchComponent implements  OnInit {
    sorting  = [{name:'Decreasing stars', val:"stars"},{name:'Increasing stars',val:"-stars"},
        {name:'Decreasing pulls', val:"pulls"},{name:'Increasing pulls',val:"-pulls"},
        {name:'Increasing stars  Increasing pulls', val:"-stars -pulls"}
    ];

    comparisons = [{name:">=", val:"_gt"},{name:"<",val:"_lt"},{name:"=",val:""}];


     softwares : Software [] = [ new Software("", "", false)]; //{software:'', version:'', error:false}];
     msg: string = '';

    
     selectedSort = {name:"sort", val:"stars"}; //default selection od sorting (Descreaing order)

     sizeCmpValue =  {name:"size",  cmp: this.comparisons[0].val, val:"0"};  //size_gt=x, size_lt=y, size=z
     pullsCmpValue = {name:"pulls", cmp: this.comparisons[0].val, val:"0"};
     starsCmpValue = {name:"stars", cmp: this.comparisons[0].val, val:"0"};

     availableSoftware : string [] =["java", "python","pip", "wget",'perl','nano',
                'php','ruby','scala','groovy','apache2','nginx','nodejs','npm','gunicorn','curl'];

    resultImages : Image[];
    count = 0;
    //
     constructor( private imageService: ImageService,
                  private router: Router){
                 // private softwareService: SoftwareService){
    //      //this.softwares.push(new Software("", ""));
    //       this.selectedSort.val = this.sorting[0].val;
     }
    
    ngOnInit(): void {
        //availableSoftwre
            
    }
    remove(id: number) {
        this.softwares.splice(id, 1);
    }
    
    add(id){
        this.softwares.push(new Software("", "", false));
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
        // //this.constructSearchUrl();
        // this.imageService.searchImages(this.constructSearchUrl())
        //     .then(images=>{
        //          if(images.length > 0 ) {
        //             this.resultImages = images;
        //             this.count = images.length;
        //             console.log(images);
        //         }
        //     });   //res in the json
        let link = ['/images', this.constructSearchUrl()];
        this.router.navigate(link);
    }

    constructSearchUrl(){
        var url_search ="";
        for(var sw of this.softwares){
            url_search +=sw.name+"="+sw.version+"&";
            console.log("VERSION:"+sw.version+"########")
        }
        url_search += "sort="+this.selectedSort.val;
        url_search += "&"+this.sizeCmpValue.name+this.sizeCmpValue.cmp+"="+this.sizeCmpValue.val;
        url_search += "&"+this.pullsCmpValue.name+this.pullsCmpValue.cmp+"="+this.pullsCmpValue.val;
        url_search += "&"+this.starsCmpValue.name+this.starsCmpValue.cmp+"="+this.starsCmpValue.val;

        return url_search;
    }


}

