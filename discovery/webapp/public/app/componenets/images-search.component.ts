/**
 * Created by dido on 7/10/16.
 */
import {Component, OnInit, Input}      from '@angular/core';

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
        {name:'Increasing stars  Increasing pulls', val:"-stars&sort=-pulls"}
    ];

    comparisons = [{name:">=", val:"_gt"},{name:"<",val:"_lt"},{name:"=",val:""}];

    //list  software and version used to construct the search URL
    softwares : Software [] = [ new Software("", "", false)];
    //{software:'', version:'', error:false}];
    msg: string = '';


     selectedSort = {name:"sort", val:"stars"}; //default selection of sorting (Decresing order)

     sizeCmpValue =  {name:"size",  cmp: this.comparisons[0].val, val:"0"};  //size_gt=x, size_lt=y, size=z
     pullsCmpValue = {name:"pulls", cmp: this.comparisons[0].val, val:"0"};
     starsCmpValue = {name:"stars", cmp: this.comparisons[0].val, val:"0"};

     availableSoftware : string [] =["java", "python","pip", "wget",'perl','nano','php','ruby','scala','groovy',
                                     'apache2','nginx','nodejs','npm','gunicorn','curl','unzip', 'tar','zip','erl',
                                     'go','ash','zsh','bash','git','ping','gradle','mvn'];

    resultImages : Image[];
    count = 0;
    //
     constructor( private imageService: ImageService,
                  private router: Router){

                //    sizeCmpValue =  {name:"size",  cmp: this.comparisons[0].val, val:"0"};

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

    ngAfterViewInit(): void{
    //  console.log("CALLED NGAFTERVIEW INIT")
      let param = this.imageService.getSearchQueryParameters()
      console.log(param.toString())

      this.availableSoftware.forEach(name => {
          if (param.has(name)){
            console.log(this.softwares[0]['name'])
            if(this.softwares[0]['name']){
              console.log(param.get(name));
              this.softwares.push(new Software(name,param.get(name), false));
            }
            else{
              this.softwares[0] = new Software(name,param.get(name), false)
            }
          }
      });
      //java=1.8&python=2.7&sort=stars&size_lt=0&pulls_gt=0&stars_gt=0

      //set the selected sort
      this.selectedSort.val=  param.get(this.selectedSort.name)

      //size_lt, size_gt, size
      //pulls_gt, pulls_gt, pulls
      //stars_gt, stars_gt, stars
      if (param.has("stars")){
        this.starsCmpValue.cmp = this.comparisons[2].val;
        this.starsCmpValue.val = param.get("stars");
      }
      if (param.has("stars_lt")){
        this.starsCmpValue.cmp = this.comparisons[1].val;
        this.starsCmpValue.val = param.get("stars_lt");
      }
      if (param.has("stars_gt")){
        this.starsCmpValue.cmp = this.comparisons[0].val;
        this.starsCmpValue.val = param.get("stars_gt");
      }
      if (param.has("pulls")){
        this.pullsCmpValue.cmp = this.comparisons[2].val;
        this.pullsCmpValue.val = param.get("pulls");
      }
      if (param.has("pulls_lt")){
        this.pullsCmpValue.cmp = this.comparisons[1].val;
        this.pullsCmpValue.val = param.get("pulls_lt");
      }
      if (param.has("pulls_gt")){
        this.pullsCmpValue.cmp = this.comparisons[0].val;
        this.pullsCmpValue.val = param.get("pulls_gt");
      }
      if (param.has("size")){
        this.sizeCmpValue.cmp = this.comparisons[2].val;
        this.sizeCmpValue.val = param.get("size");
      }
      if (param.has("size_lt")){
        this.sizeCmpValue.cmp = this.comparisons[1].val;
        this.sizeCmpValue.val = param.get("size_lt");
      }
      if (param.has("size_gt")){
        this.sizeCmpValue.cmp = this.comparisons[0].val;
        this.sizeCmpValue.val = param.get("size_gt");
      }
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
            //console.log("Versione: "+sw.version)
        }
        // console.log("$$$$$$$$$$$ VALUE"+ this.selectedSort.val +"#####");

        if (this.selectedSort.val ===  null)
          url_search += "sort=stars";
        else
          url_search += "sort="+this.selectedSort.val;
        url_search += "&"+this.sizeCmpValue.name+this.sizeCmpValue.cmp+"="+this.sizeCmpValue.val;
        url_search += "&"+this.pullsCmpValue.name+this.pullsCmpValue.cmp+"="+this.pullsCmpValue.val;
        url_search += "&"+this.starsCmpValue.name+this.starsCmpValue.cmp+"="+this.starsCmpValue.val;
        console.log("Search: "+url_search)
        return url_search;
    }


}
